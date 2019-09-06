# -*- coding: utf-8 -*-
import json

import scrapy
import scrapy
from scrapy.loader import ItemLoader
from Scrapy_spider.items import MaiGooItem


class MaigooSpiderSpider(scrapy.Spider):
    name = 'maigoo_spider'
    allowed_domains = ['maigoo.com']
    start_urls = ['http://www.maigoo.com/']

    def parse(self, response):
        item_loader = ItemLoader(item=MaiGooItem(), response=response)
        # 导航页的chatid抓下来，对应的导航链接是https://www.maigoo.com/?action=getbelow&catid=5
        catid = response.xpath('//div[@id="menubox"]//li/@catid').extract()
        for index, navigation_id in enumerate(catid):
            # 进入分类中的各个导航页面
            navigation_name = response.xpath('//div[@id="menubox"]//li/a/text()').extract()[index]
            navigation_link = 'https://www.maigoo.com/?action=getbelow&catid={id}'.format(id=navigation_id)
            item_loader.add_value('trademark_throng', navigation_name)
            item_loader.add_value('trademark_address', navigation_link)
            # 会将ressponse插入mongo后，返回Mongo_id，插入到mysql中
            item_loader.add_value('mongo_id', json.dumps(response.text))

            article_item = item_loader.load_item()
            yield article_item


    def parse_navigation_response(self, response):
        item_loader = ItemLoader(item=MaiGooItem(), response=response)
        # 这种写法可以将需要的字段写入数据库，后面可以进行动态的配置
        # 可以帮助判断取出来的值是否为空，自己无需做判断
        item_loader.add_xpath('catid', response.xpath('//div[@id="menubox"]//li/@catid').extract())
        item_loader.add_value('catid', '')

        # 调用load_item  进行解析
        article_item = item_loader.load_item()
        yield article_item

