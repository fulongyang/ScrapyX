# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy_redis.spiders import RedisSpider
from Scrapy_RedisSpider.items import ZhaoShanItem, get_region_name_id, alter_price, get_trademard_fid_id_fid_name


class Jmw91spiderSpider(RedisSpider):
    name = 'Jmw91Spider'
    allowed_domains = ['91jmw.com']
    start_urls = ['https://www.91jmw.com/list/c0_f0_a0_k_p1']

    redis_key = 'Jmw91Spider:Jmw91SpiderQueue'
    
        

    def start_requests(self):
        """Returns a batch of start requests from redis."""
        yield scrapy.Request(url=self.start_urls[0])


    def parse(self, response):
        #------递归下一页自己
        next_page_items_first = response.xpath('//div[@class="pager"]/a[contains(@title,"下一页")]/@href').extract()
        next_page_items = response.xpath('//div[@class="pager"]/a/@href').extract() if not next_page_items_first else next_page_items_first
        # next_page_items_link = 'https://www.91jmw.com'+''.join(next_page_items) if next_page_items else None
        next_page_items_links = list(map(lambda x:'https://www.91jmw.com'+x,next_page_items))
        for next_page_items_link in next_page_items_links:
            yield scrapy.Request(url=next_page_items_link, callback=self.parse, dont_filter=False,
                                 meta={})


        #------回调当前页给解析函数
        next_items = response.xpath('//div[@class="prd-list full "]')
        for next_item in next_items:
            next_link = next_item.xpath('//div[@class="div-img "]/a/@href').extract()
            next_link_urls = ['https://www.91jmw.com'+link_part for link_part in next_link if link_part]
            for next_link_url in next_link_urls:
                print(next_link_url)
                yield scrapy.Request(url=next_link_url, callback=self.parse_items, dont_filter=False,
                                 meta={})


    def parse_items(self,response):
        zhaoshan_items = ZhaoShanItem()
        items = {}
        items['title']=response.xpath('//div[@class="project-name"]/h2/text()').re('【(.*?)】')# '品牌名稱',
        items['spider_url']= 'https://www.91jmw.com'  #'爬取网站',

        items['region_name']=response.xpath('*//div[@class="project-info"][1]/p[5]').xpath('string(.)').get(default='').split()[-1:]#'省份名',
        items['region'] =list(map(lambda x:get_region_name_id(x),[items['region_name']]))[0].get('get_region_id') #'省份',

        items['companyname']=response.xpath('*//div[@class="prd-item"][3]/p[1]').xpath('string(.)').get(default='').split()[-1:] #'公司名称',
        items['fid_name']=response.xpath('*//div[@class="project-info"][1]/p[4]').xpath('string(.)').get(default='').split()[2:]#'分类名称',
        items['fid_name']=list(map(lambda x:x.replace('>',''),items['fid_name']))#'分类名称',


        # items['fid']=list(map(lambda x:get_trademard_fid_id_fid_name(x),items['fid_name']))[0].get('fid_id') if items['fid_name'] else ''#'分类id',
        items['source']=response.xpath('*//div[@class="project-info"][1]/p[5]').xpath('string(.)').get(default='').split()[2:]#'品牌发源地/公司地址',
        # items['contents']='招商全部',
        items['content']= response.xpath('//div[@class="jiameng-d-step cont-jiameng "]/div[1]').get(default='') #'加盟详情',
        # items['manage']='经营范围',
        # items['foundtime']='品牌创立时间',
        items['shopnum']= response.xpath('*//div[@class="project-info"][1]/p[2]').xpath('string(.)').re('(\d+)家') #'门店总数',
        # items['trademark_all_img']= '品牌所有图片',
        items['advantage']=response.xpath('//div[@class="jiameng-d-step cont-jiameng "]/div[3]').get(default='') # '加盟优势',
        items['slideshow']= response.xpath('//img[@class="lazyload"]/@data-src').get(default='') #'产品log图',
        # items['process']= '加盟流程',
        # items['analysis']= '加盟费分析',
        # items['conditions']= '加盟条件',
        # items['telephone']= '固定电话',
        # items['mobilephone']= '移动手机',
        # items['email']= '邮箱地址',
        # items['fax']= '公司传真',
        # items['corporation']= '公司法人',
        # items['unite']= '统一社会信用代码',
        # items['websiteurl']= '品牌官网网址',
        # items['grade']= '品牌评分',
        # items['trademark_img']= '品牌图片',
        items['trademark_cp']= response.xpath('*//div[@class="project-info"][1]/p[3]').xpath('string(.)').get(default='')#'品牌产品',
        items['trademark_address']= response.xpath('*//div[@class="prd-item"][3]/p[3]').xpath('string(.)').get(default='').split()[-1:] #'公司地址',
        items['trademark_throng']= response.xpath('*//div[@class="project-info"][1]/p[7]').xpath('string(.)').get(default='').split()[2:]#'适合人群',
        items['mongo_id']= response.text #'mongo_id',
        items['feeid']=response.xpath('//span[@class="fl p-price"]').xpath('string(.)').re('￥(.*?)万')# '加盟价钱',
        items['feeid']=list(map(lambda x:alter_price(x),items['feeid'])) if all([isinstance(items['feeid'],list)]) else ''# '加盟价钱',

        # items['pattern']= '经营模式',
        # items['title_picture']= '品牌商标图片',
        # items['jiamengnum']= '加盟人数',
        items['thumb']= response.xpath('//ul[@class="scroll_pic cls"]/li//img/@src').getall() #'轮播图',
        # items['update_biaoshi']= '1 =上传至oss',
        items['url']=response.url # '网站url',
        items_0 = {k:list(map(lambda x:x.replace('>',''),v)) if k=='fid_name' else v for k, v in items.items()}
        items_1 = {k:','.join(v) if isinstance(v,list) else v for k, v in items_0.items() if v}
        items_2 = {k:'' if all([k=='slideshow','pro_91' in v]) else v for k, v in items_1.items()}
        zhaoshan_items.update(items_2)
        yield zhaoshan_items












