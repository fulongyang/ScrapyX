# -*- coding: utf-8 -*-
import random

import scrapy
from scrapy_redis.spiders import RedisSpider

from Scrapy_RedisSpider.items import ZhaoShanItem, get_region_name_id, AlterClassify, alter_price


class AnxjmspiderSpider(AlterClassify,RedisSpider):
    name = 'AnxjmSpider'
    allowed_domains = ['anxjm.com']
    start_urls = ['https://www.anxjm.com/search/1/']
    redis_key = 'AnxjmSpider:AnxjmSpiderQueue'


    def __init__(self):
        super(AnxjmspiderSpider,self).__init__()
       

    def start_requests(self):
        """Returns a batch of start requests from redis."""
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse,dont_filter=True,)

    def parse(self, response):
        #--------------回调给解析函数
        next_item_links = list(map(lambda x:'https://www.anxjm.com'+x,response.xpath('//div[@class="titBox"]/h2/a/@href').extract()))
        for next_item_link in next_item_links:
            yield scrapy.Request(url=next_item_link, callback=self.parse_item, dont_filter=False,
                                 meta={})

        #-------------递归下一页
        next_pages = response.xpath('//ul[@class="pagination"]/li/a[contains(text(),"下一页")]/@href').get()
        yield scrapy.Request(url=next_pages, callback=self.parse, dont_filter=False,
                             meta={})

    def parse_item(self,response):
        try:
            zhaoshang_dict = {}
            # alter =AlterClassify ()
            zhaoshang_dict['title']=response.xpath('//div[@class="context_title"]/h1/text()').get() #'招商名稱',
            # zhaoshang_dict['foundtime']='品牌创立时间',
            zhaoshang_dict['spider_url']= 'https://www.anxjm.com/' #'爬取网站',

            zhaoshang_dict['region_name']= response.xpath('//ul[@class="basic_others"]/li[2]/span/text()').get() #'省份名',
            zhaoshang_dict['region'] =list(map(lambda x:get_region_name_id(x),[zhaoshang_dict['region_name']]))# '省份',
            zhaoshang_dict['region'] =zhaoshang_dict['region'][0].get('get_region_id') # '省份',
            zhaoshang_dict['companyname']= response.xpath('//li[@class="fline"][1]/span/text()').get()#'公司名称',
            zhaoshang_dict['fid_name']= response.xpath('//div[@class="path"]//a/text()').extract()[::-1][:2] #'分类名称',
            zhaoshang_dict['fid']=self.get_trademard_fid_id_fid_name(zhaoshang_dict['fid_name']).get('fid_id') #'分类id',
            zhaoshang_dict['source']= response.xpath('//ul[@class="basic_others"]/li[2]/span/text()').get() #'品牌发源地/公司地址',
            zhaoshang_dict['shopnum']=response.xpath('//li[@class="fline"][3]/span/text()').get()# '门店总数',
            # zhaoshang_dict['trademark_all_img']= '品牌所有图片',
            zhaoshang_dict['slideshow']= list(map(lambda x:'https://www.anxjm.com'+x,response.xpath('//div[@class="img-block"]/img/@src').extract()))#'产品log图',
            zhaoshang_dict['contents']=list(map(lambda x:x.split('<h2>'),response.xpath('//div[@class="body_tit"]').extract()))# '招商全部',
            zhaoshang_dict['contents']=list(map(lambda xs:'<h2>'+xs,zhaoshang_dict['contents'][0][1:]))# '招商全部',

            zhaoshang_dict['advantage']= zhaoshang_dict['contents'][3] if len(zhaoshang_dict['contents'])>3 else '' #'加盟优势',
            zhaoshang_dict['content']= zhaoshang_dict['contents'][0] if len(zhaoshang_dict['contents'])>0 else ''#'加盟详情',
            zhaoshang_dict['manage']=response.xpath('//li[@class="clear"][2]/strong/text()').get() # '经营范围',
            zhaoshang_dict['process']= zhaoshang_dict['contents'][4] if len(zhaoshang_dict['contents'])>4 else ''#'加盟流程',
            zhaoshang_dict['analysis']= zhaoshang_dict['contents'][1] if len(zhaoshang_dict['contents'])>1 else ''#'加盟费分析',
            zhaoshang_dict['conditions']= zhaoshang_dict['contents'][2] if len(zhaoshang_dict['contents'])>2 else '' #'加盟条件',

            # zhaoshang_dict['telephone']= '固定电话',
            # zhaoshang_dict['mobilephone']= '移动手机',
            # zhaoshang_dict['email']='邮箱地址',
            # zhaoshang_dict['fax']='公司传真',
            # zhaoshang_dict['corporation']='公司法人',
            # zhaoshang_dict['unite']='统一社会信用代码',
            # zhaoshang_dict['websiteurl']= '品牌官网网址',
            # zhaoshang_dict['grade']='品牌评分',
            # zhaoshang_dict['trademark_img']='品牌图片',
            # zhaoshang_dict['trademark_cp']='品牌产品',
            zhaoshang_dict['trademark_address']=response.xpath('//li[@class="clear"][3]/strong/text()').get() #,'公司地址',
            zhaoshang_dict['trademark_throng']= response.xpath('//li[@class="clear"][1]/span/text()').get()#'适合人群',
            zhaoshang_dict['mongo_id']=response.text # 'mongo_id',
            zhaoshang_dict['feeid']=alter_price(list(map(lambda x:x.split('万')[0],response.xpath('//span[@class="money"]/text()').extract()))) #'加盟价钱',
            zhaoshang_dict['pattern']=response.xpath('//li[@class="clear"][2]/span/text()').get()# '经营模式',
            # zhaoshang_dict['title_picture']= '品牌商标图片',
            zhaoshang_dict['jiamengnum']=random.randint(1,1000) #'加盟人数',
            # 'insert_time': '数据插入时间',
            zhaoshang_dict['thumb']= list(map(lambda x:'https://www.anxjm.com'+x,response.xpath('//div[@class="bd"]/ul//li/img/@src').extract()))#'轮播图',
            # zhaoshang_dict['update_biaoshi']= '1:上传至oss',
            zhaoshang_dict['url']=response.url #'网站url',

            zhaoshang_dict1 = {k:','.join(v) if isinstance(v,list) else v for k,v in zhaoshang_dict.items()}
            
            zhaoshang_result = ZhaoShanItem()
            zhaoshang_result.update(zhaoshang_dict1)
            yield zhaoshang_result
        except ValueError as e:
            print(e)


















