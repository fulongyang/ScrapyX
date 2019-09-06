# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider

from Scrapy_RedisCrawlSpider.items import GlobrandRedisCrawlSpider
start = '*'*10

class GlobrandrediscrawlspiderSpider(RedisCrawlSpider):
    name = 'GlobrandRedisCrawlSpider'
    # allowed_domains = ['china.globarand.com']
    # start_urls = ['http://china.globarand.com/join']
    
    
    redis_key = 'GlobrandRedisCrawlQueue:GlobrandRedisCrawlQueue'
    
    
    rules = (
        # Rule(LinkExtractor(restrict_xpaths=('//div[@class="itemtitle"]/a/@href',)), callback='parse_item', follow=False),
        # Rule(LinkExtractor(restrict_xpaths=('//div[@class="page"]/a/@href',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('/brand/.*?/')), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=('/join/\d+/')), callback='parse_item', follow=True),
    )



    def parse_item(self, response):

        page_item_link = response.xpath('//div[@class="itemtitle"]/a/@href').getall()
        titles= response.xpath('//div[@class="itemtitle"]/a/text()').getall()
        for index,item_link,item_title in zip(range(1,len(page_item_link)),page_item_link,titles):
            # for i, c, d in zip(range(1, len(a)), a, b):
            now_item = response.xpath('//div[contains(@class,"item")][{}]'.format(index)).get()
            yield scrapy.Request(url=item_link, callback=self.parse_page_source,meta={'title':item_title,'item':now_item})



    def parse_page_source(self,response):
        item = GlobrandRedisCrawlSpider()
        node_item = response.meta.get('item')
        title = response.meta.get('title')
        item['url'] = response.url
        item['mongo_id'] = {'scorcedata':json.dumps(response.text),'node_item':node_item,}
        item['title'] = title
        return item
        # now_item = response.xpath('//div[@class="item"]').getall()
       














