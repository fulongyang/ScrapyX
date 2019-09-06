# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy_redis.spiders import RedisSpider
from Scrapy_RedisSpider.items import ZhaoShanItem, get_trademard_fid_id_fid_name,get_region_name_id,alter_price
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from Scrapy_RedisSpider.items import CompanyItems





class BaiducompanyspiderSpider(RedisSpider):
    name = 'BaiduCompanySpider'
    # allowed_domains = ['xin.baidu.com']
    # start_urls = ['https://xin.baidu.com/mark?q=%E9%B9%8F%E8%AE%AF&t=7']
    redis_key = 'BaiduCompanySpider:BaiduCompanySpiderQueue'



    def parse(self, response):
        items = CompanyItems()
        items['company_name'] = 'aaa'
        items['maigoo_company_mongo_id'] = json.dumps(response.text)
        return items






































