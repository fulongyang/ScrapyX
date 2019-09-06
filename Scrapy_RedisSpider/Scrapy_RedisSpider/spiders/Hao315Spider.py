# -*- coding: utf-8 -*-
import scrapy

from Scrapy_RedisSpider.items import ZhaoShanItem, AlterClassify

from scrapy_redis.spiders import RedisSpider

class Hao315spiderSpider(AlterClassify,RedisSpider):
    name = 'Hao315Spider'
    allowed_domains = ['hao315.com']
    start_urls = ['http://jm.hao315.com/class/7_0_0_0_1.html']
    redis_key = 'Hao315Spider:Hao315SpiderQueue'
    
    def __init__(self):
        super().__init__()
        

    # def start_requests(self):
    #     """Returns a batch of start requests from redis."""
    #     yield scrapy.Request(url=self.start_urls[0])
    
    
    def parse(self, response):
        #--------------next items
        next_page_items_links=response.xpath('*//div[contains(@class,"prod_introduce")]')
        for next_page_items_links_ in next_page_items_links:
            next_page_items_link = next_page_items_links_.xpath('h5[contains(@class,"prod_h5_bt")]/a/@href').get()

            yield scrapy.Request(url=next_page_items_link, callback=self.parse_items, dont_filter=False,
                                 meta={'up_page':response.url})


        #------------next page
        next_link_urls=response.xpath('//div[contains(@class,"turn_page")]//a/@href').extract()
        for next_link_urls_ in next_link_urls:
            next_link_url = 'http://jm.hao315.com{}'.format(next_link_urls_)
            yield scrapy.Request(url=next_link_url, callback=self.parse, dont_filter=False,
                             meta={})


    def parse_items(self, response):
        ZhaoShanItem_items = ZhaoShanItem()
        zhaoshang_dict = {}
        try:
            zhaoshang_dict['title'] = response.xpath('//table[contains(@class,"left_03_one_table")]//tr[1]//td[2]/text()').get()  # 品牌名稱
            zhaoshang_dict["spider_url"] = 'http://jm.hao315.com'  # 爬取网站
            zhaoshang_dict["region_name"] = response.xpath('//table[contains(@class,"left_03_one_table")]//tr[1]//td[4]/text()').get()  # 省份名
            zhaoshang_dict["region"] = list(map(lambda x:self.get_region_name_id(x),[zhaoshang_dict['region_name']]))[0].get('get_region_id','')# 省份
            zhaoshang_dict["companyname"] = response.xpath('//p[contains(text(),"企业名称")]/a/text()').get()  # 公司名称
            zhaoshang_dict["fid_name"] = response.xpath('//div[contains(@class,"Index_one_02 clearfix fl")]/p[2]/text()').get().split('>')[::-1][:2]  # 分类名称
            zhaoshang_dict["fid"] = self.get_trademard_fid_id_fid_name(zhaoshang_dict['fid_name']).get('fid_id') # 分类id
            zhaoshang_dict["source"] = response.xpath('//p[contains(text(),"企业地址")]/text()').get().split('：')[-1:]  # 公司地址
            # zhaoshang_dict["contents"] = response.xpath(" ")  # 招商全部
            # zhaoshang_dict["content"] = response.xpath('//div[@class="Index_cen_four_left_03_two"]').get()  # 加盟详情
            # zhaoshang_dict["manage"] = response.xpath('//table[contains(@class,"left_03_one_table")]//tr[3]//td[4]/text()')  # 经营范围
            # zhaoshang_dict["foundtime"] = response.xpath(" ")  # 品牌创立时间

            # zhaoshang_dict["shopnum"] = response.xpath(" ")  # 门店总数
            # zhaoshang_dict["trademark_all_img"] = response.xpath(" ")  # 品牌所有图片  '企业地址：北京市朝阳区南磨房路'
            # zhaoshang_dict["advantage"] = response.xpath(" ")  # 加盟优势
            zhaoshang_dict["slideshow"] = response.xpath('//div[contains(@class,"Index_one_01 clearfix fl")]/a/img/@src').get()  # 产品log图

            # zhaoshang_dict["process"] = response.xpath(" ")  # 加盟流程
            # zhaoshang_dict["analysis"] = response.xpath(" ")  # 加盟费分析
            # zhaoshang_dict["conditions"] = response.xpath(" ")  # 加盟条件
            # zhaoshang_dict["telephone"] = response.xpath(" ")  # 固定电话
            # zhaoshang_dict["mobilephone"] = response.xpath(" ")  # 移动手机
            # zhaoshang_dict["email"] = response.xpath(" ")  # 邮箱地址
            # zhaoshang_dict["fax"] = response.xpath(" ")  # 公司传真
            # zhaoshang_dict["corporation"] = response.xpath(" ")  # 公司法人
            # zhaoshang_dict["unite"] = response.xpath(" ")  # 统一社会信用代码
            # zhaoshang_dict["websiteurl"] = response.xpath(" ")  # 品牌官网网址
            # zhaoshang_dict["grade"] = response.xpath(" ")  # 品牌评分
            # zhaoshang_dict["trademark_img"] = response.xpath(" ")  # 品牌图片
            # zhaoshang_dict["trademark_cp"] = response.xpath(" ")  # 品牌产品
            # zhaoshang_dict["trademark_address"] = response.xpath(" ")  # 公司地址
            # zhaoshang_dict["trademark_throng"] = response.xpath(" ")  # 适合人群
            zhaoshang_dict["mongo_id"] = response.text  # mongo_id
            zhaoshang_dict["feeid"] = response.xpath('//div[contains(@class,"Index_one_02 clearfix fl")]/p[2]/text()[2]').extract()  # 加盟价钱
            # zhaoshang_dict["pattern"] = response.xpath(" ")  # 经营模式
            # zhaoshang_dict["title_picture"] = response.xpath(" ")  # 品牌商标图片
            # zhaoshang_dict["jiamengnum"] = response.xpath(" ")  # 加盟人数
            # zhaoshang_dict["insert_time"] = response.xpath(" ")  # 数据插入时间
            zhaoshang_dict["thumb"] = response.xpath('//div[contains(@class,"Index_cen_three_01 fl")]/ul/li/a/img/@src').extract()  # 轮播图
            # zhaoshang_dict["update_biaoshi"] = response.xpath(" ")  # 1:上传至oss
            zhaoshang_dict["url"] =[response.meta.get('up_page'),response.url]  # 网站url
        except Exception as e:
            print(e)
        zhaoshang_dicts = {k:','.join(v) if isinstance(v,list) else v for k, v in zhaoshang_dict.items()}
        ZhaoShanItem_items.update(zhaoshang_dicts)
        yield ZhaoShanItem_items
        
        
        
        