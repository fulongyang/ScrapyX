# -*- coding: utf-8 -*-
from collections import OrderedDict

import scrapy
from scrapy.loader import ItemLoader

from Scrapy_RedisSpider.items import ZhaoShanItem


class Jx3158SpiderSpider(scrapy.Spider):
    name = 'JX_3158_Spider'
    # allowed_domains = ['http://www.hao315.cn/']
    start_urls = ['https://www.3158.cn']



    def parse(self, response):
        #--------------递归回调主页面给自己
        next_links = response.xpath('//ul[@class="side-ul"]//li/div[@class="list-item"]/a/@href').getall()
        if next_links:
            next_link = list(map(lambda x:'https:'+x+'?pt=all',next_links))
            for next_item_link in next_link:
                yield scrapy.Request(url=next_item_link, callback=self.parse, dont_filter=False,
                                     meta={})

        
        #--------------递归给自己
        next_items_links = response.xpath('//ul[@class="xm-list clearfix"]/li')
        if next_items_links:
            for parse_next_item in next_items_links:
                parse_items_links = parse_next_item.xpath('@data-link').extract()
                result_items_links = list(map(lambda x: 'https:' + x if not x.startswith('https') else x, parse_items_links))
                description = parse_next_item.xpath('*//p[@class="txt"]/text()').get()
                for index,next_parse_link in enumerate(result_items_links):
                    yield scrapy.Request(url=next_parse_link, callback=self.parse, dont_filter=False,
                                         meta={'description':description})


        # ---------------递归出口 回调给解析函数
        goto_item_detail = response.xpath('//li[@class="zsdetail"]/a/@href').get()
        if goto_item_detail:
            goto_item_detail_link = 'https://www.3158.cn' + goto_item_detail if isinstance(goto_item_detail,str) else None
            description = response.meta.get('description', '')
            if goto_item_detail_link:
                yield scrapy.Request(url=goto_item_detail_link, callback=self.parse_items, dont_filter=False,
                                     meta={'description': description})


    def parse_items(self,response):

        title = response
        if title:
            item = ZhaoShanItem()
            item_loader = ItemLoader(item=item, response=response)
            zhaoshang_dicts = OrderedDict()
            zhaoshang_dicts["time"] = response.xpath(" ")  # string请求时间戳
            zhaoshang_dicts["title"] = response.xpath('//div[@class="detailTitle mt10 clearfix"]/b/text()').get()  # string招商标题
            zhaoshang_dicts["feeid"] = response.xpath(" ")  # string加盟费用
            zhaoshang_dicts["thumb"] = response.xpath(" ")  # string 	缩略图远程地址
            zhaoshang_dicts["keyword"] = response.xpath(" ")  # string 	关键字
            zhaoshang_dicts["description"] = response.meta.get('description', '')  # string 	招商描述
            zhaoshang_dicts["slideshow"] = response.xpath(" ")  # array 轮播图片远程地址
            zhaoshang_dicts["region"] = response.xpath(" ")  # int 	地区
            zhaoshang_dicts["author"] = response.xpath(" ")  # string 	作者
            zhaoshang_dicts["count "] = response.xpath(" ")  # int 	浏览量
            zhaoshang_dicts["pp_cid"] = response.xpath(" ")  # string 	分类ID
            zhaoshang_dicts["manage"] = response.xpath(" ")  # string 	经营产品
            zhaoshang_dicts["pattern"] = response.xpath(" ")  # string 	经营模式
            zhaoshang_dicts["source"] = response.xpath(" ")  # string 	品牌源地
            zhaoshang_dicts["shopnum"] = response.xpath(" ")  # int 	店铺数量
            zhaoshang_dicts["jiamengnum"] = response.xpath(" ")  # int 	加盟人数
            zhaoshang_dicts["content"] = response.xpath(" ")  # string 	加盟详情
            zhaoshang_dicts["advantage"] = response.xpath(" ")  # string 	加盟优势
            zhaoshang_dicts["analysis"] = response.xpath(" ")  # string 	加盟费分析
            zhaoshang_dicts["conditions"] = response.xpath(" ")  # string 	加盟条件
            zhaoshang_dicts["process"] = response.xpath(" ")  # string 	加盟流程
            zhaoshang_dicts["picture"] = response.xpath(" ")  # array 	产品图片远程地址
            

            item_keys = list(item.zhaoshang_dict_word02.keys())
            for item_key in item_keys:
                item_loader.add_xpath(item_key, '//div[@class="product_name"]')
                
            article_item = item_loader.load_item()
            article_item.update(zhaoshang_dicts)
            return article_item















def helper():
    zhaoshang_dict_word02 = {
        'time': 'string请求时间戳',
        'title': 'string招商标题',
        'feeid': 'string加盟费用',
        'thumb': 'string 	缩略图远程地址',
        'keyword': 'string 	关键字',
        'description': 'string 	招商描述',
        'slideshow': 'array 轮播图片远程地址',
        'region': 'int 	地区',
        'author': 'string 	作者',
        'count ': 'int 	浏览量',
        'pp_cid': 'string 	分类ID ',
        'manage': 'string 	经营产品',
        'pattern': 'string 	经营模式',
        'source': 'string 	品牌源地',
        'shopnum': 'int 	店铺数量',
        'jiamengnum': 'int 	加盟人数',
        'content': 'string 	加盟详情',
        'advantage': 'string 	加盟优势',
        'analysis': 'string 	加盟费分析',
        'conditions': 'string 	加盟条件',
        'process': 'string 	加盟流程',
        'picture': 'array 	产品图片远程地址',
    }

    for k1, v1 in zhaoshang_dict_word02.items():
        print('zhaoshang_dicts["{}"] = response.xpath(" ") #{}'.format(k1, v1))





if __name__ == "__main__":
    helper()








