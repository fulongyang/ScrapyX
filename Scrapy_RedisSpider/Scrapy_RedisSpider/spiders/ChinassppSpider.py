# -*- coding: utf-8 -*-
import scrapy
import json
import random
import re
from urllib.parse import unquote
from scrapy_redis.spiders import RedisSpider
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote
from Scrapy_RedisSpider.items import MaiGooItem, get_trademard_fid_id_fid_name, get_region_name_id, GetMysqlV3
star = '*'*10

from queue import Queue

url_queue = Queue()

class ChinassppspiderSpider(RedisSpider):
    name = 'ChinassppSpider'
    # allowed_domains = ['chinasspp.com']
    # start_urls = ['http://www.chinasspp.com/brand/bsearch.aspx?area=%E5%AE%89%E5%BE%BD%E7%9C%81&page=7']
    redis_key = 'ChinassppSpider:ChinassppSpiderQueue'

    # rules = (
    #     # Rule(LinkExtractor(restrict_xpaths=('//div[@class="page"]/a/@href',)), callback='parse_item', follow=True),
    #     Rule(LinkExtractor(allow=('.*?area=\w+.*?')), callback='start_parse', follow=False),
    #     Rule(LinkExtractor(allow=('http://.*?area=.*?page=\d+')), callback='parse_item', follow=True),
    #     
    # )
    set_url = set()
    # def start_requests(self):
    #     """Returns a batch of start requests from redis."""
    #     yield scrapy.Request(url=self.start_urls[0])

    def parse(self, response):

        #-------切换省份
        region_urls = response.xpath('//div[@id="sift"]/p[3]/span//a/@href').getall()
        for region_url in region_urls:
            if region_url not in self.set_url:
                self.set_url.add(region_url)
                print('切换省份',unquote(region_url))
                yield scrapy.Request(url=region_url, callback=self.parse, dont_filter=False,
                                     meta={'region': '', })


        #------------------翻页回 递归给自己
        if response.url not in self.set_url:
            self.set_url.add(response.url)
            page_int = response.xpath('//p[@id="l_page"]/a/@href').getall()
            max_int = max([int(re.findall('page=(\d+)', p)[0]) for p in page_int] if page_int else [1])
            for page_num in range(max_int,-1,-1):
                re_url = re.sub('page=(\d+)', 'page={}', response.url).format(page_num+1)
                if re_url not in self.set_url:
                    self.set_url.add(re_url)
                    print('回调翻页给自己',re_url)
                    url_queue.put(re_url)
                    # yield scrapy.Request(url=re_url, callback=self.parse, dont_filter=False,
                    #                      meta={'region': '', })
        next_url = url_queue.get()
        print(type(next_url))
        yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=False,
                             meta={})

        #------------当前页回调给解析函数
        print(star,'当前url',unquote(response.url))

        items = response.xpath('//div[@class="brand"]')
        for item in items:
            next_item_link  = item.xpath('./a/@href').get()
            next_item_title  = item.xpath('./a/@title').get()
            if next_item_link not in self.set_url:
                self.set_url.add(next_item_link)

                #------------------mysql 去重
                get_mysql = GetMysqlV3()
                get_mysql_data = """select id from pp_spider where title='{}' and spider_url='{}';"""
                get_mysql_sql = get_mysql_data.format(next_item_title,'http://www.chinasspp.com')
                get_mysql_querys = get_mysql.get_mysql_one(get_mysql_sql)
                print('get_mysql_sql', get_mysql_sql, 'get_mysql_query', get_mysql_querys)
                if get_mysql_querys is not None:
                    print('is in mysql !!!')
                    break
                region = unquote(re.findall('area=(.*?)&',response.url)[0])
                print(star,'回调给解析函数',next_item_link,star,next_item_title)
                yield scrapy.Request(url=next_item_link, callback=self.parse_item, dont_filter=False,
                                     meta={'region': region, 'up_response': response.url})

  



    def parse_item(self,response):
        print(star,'进入 parse_item')
        items = MaiGooItem()
        items['url'] = unquote(response.url)
        items['mongo_id'] = json.dumps(response.text)
        # need word
        items['spider_url'] = 'http://www.chinasspp.com'
        fid = response.xpath('//ul[@id="brand_info_ctl00_blink"]/li[2]/text()').get()  # 行业分类ID
        fid_id_fid_name = get_trademard_fid_id_fid_name(fid.split('-')[::-1]) if fid else {}
        items['fid'] = fid_id_fid_name.get('fid_id','')  # 行业分类ID
        items['fid_name'] = fid_id_fid_name.get('fid_name','')  #行业分类名稱

        items['title'] = response.xpath('//ul[@id="brand_info_ctl00_blink"]/li[1]/text()').get()  # 标题
        items['thumb'] = response.xpath('//p[@class="logo"]/img/@src').get()                        # 缩略图
        region_item = get_region_name_id(key=response.meta.get('region',''))
        items['region'] = region_item.get('get_region_id','')                                                             # 省份
        items['region_name'] = region_item.get('get_region_name','')                                                                     # 省份
        items['address'] = ''  # 品牌发源地
        items['foundtime'] = ''                                                                     # 品牌创立时间
        items['corporation'] = ''                                                                   # 公司法人
        items['telphone'] = 'http://www.chinasspp.com{}'.format(response.xpath('//ul[@id="brand_info_ctl00_blink"]/li[4]/img/@src').get())  # 图片固话
        items['companyname'] = response.xpath('//ul[@id="brand_info_ctl00_blink"]/li[3]/text()').get()  # 公司名称
        items['websiteurl'] = response.xpath('//ul[@id="brand_info_ctl00_blink"]/li[6]/a/@href').get()  # 官网
        items['content'] = response.xpath('//div[@class="r r_about"]').get()  # 内容
        items['slideshow'] = response.xpath('//div[@id="brand_info_ctl00_r_banner"]/ul/li/img/@src').get()  # 轮播图
        # slideshow_html_link = response.xpath('//div[@class="r r_photo"]/ul//li/a/@href | //div[@class="r r_photo"]/ul//li/a/@title').getall()

        items['bid']    =''                    # 品牌等级（500强。。。）
        items['grade']  =''                  # 品牌评分（1-5随机）
        items['scope']  =''                  # 经营范围（fid未修改前)
        items['idenid'] =1                  # 认证标签(idenid值全部为1)
        items['email']  =''                  #邮箱
        items['index_item']    =''             # 排名
        items['classify_name'] =''          # 分类名称

        # anader word
        items['corporation_link'] = response.xpath('//ul[@id="brand_info_ctl00_blink"]/li[6]/a/@href').get()   #公司介绍链接
        items['websiteurl_info']  = unquote(response.meta.get('up_response',''))           #公司网址
        items['user_comment']     = ''           #品牌评论
        items['bid_name']         = ''           #品牌等级名称
        items['update_biaoshi']   = 10
        items['company_address']   = response.xpath('//ul[@id="brand_info_ctl00_blink"]/li[6]/text()').get()
        yield items
        
    
    






