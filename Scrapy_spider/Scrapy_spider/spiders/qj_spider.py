# -*- coding: utf-8 -*-
import json

import scrapy




import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.shell import inspect_response
from bs4 import BeautifulSoup as bs
import pdb

from Scrapy_spider.items import PpSpiderItem



url_list = []


class QjSpiderSpider(scrapy.Spider):
    name = 'qj_spider'
    allowed_domains = ['qj.com.cn']
    start_urls = ['https://www.qj.com.cn/so/z010/']


    def parse(self, response):

        #----------以省份开始扩展抓取
        sf_ids = [c.split('/')[-2:-1][0] for c in
                  response.xpath('//dl[@id="select3"]//dd//a/@href').extract()]         # 省份 id
        sf_name = list(
            map(str.strip, response.xpath('//dl[@id="select3"]//dd//a').xpath('string(.)').extract()))  # 省份名字
        sf_dict = dict(zip(sf_ids, sf_name))
        find_id = response.url.split('/')[-2:-1][0]
        z = find_id.index('z') if 'z' in find_id else 2
        region = sf_dict.get(find_id[z:] if z > 1 else find_id, 'None')

        #进入省份 回调给自己
        next_sf = response.xpath('//dl[@id="select3"]//dd//a/@href').extract()[1:]
        for sf_link in next_sf:
            if sf_link not in url_list:         #list去重
                url_list.append(sf_link)
                yield scrapy.Request(url=sf_link, callback=self.parse, dont_filter=True)


        #进入页面项目链接  回调给解析
        next_items = response.xpath('//div[@class="brandimg"]/a/@href').getall()
        for next_item in next_items:
            yield scrapy.Request(url=next_item, callback=self.parse_next_item, dont_filter=True,meta={'first_page':{'region':region}})


        #进入下一页  回调给自己
        next_page = response.xpath('//div[@class="propage"]//a/@href').getall()
        for next_url in next_page:
            if next_url not in url_list:        #list去重
                url_list.append(next_url)
                yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)


    def parse_next_item(self,response):
        item = PpSpiderItem()
        item['manage']          = ','.join(response.xpath('//dl[@class="location"]').xpath('string(.)').re('>(.*)')[0].replace('\r', '').split('>')[:2])
        item['source']          =response.xpath('//div[@class="brandtxt"]//li[2]').xpath('string(.)').extract()[0].split('：')[-1:][0]
        get_region_name_id      = item.get_region_name_id(key=response.meta['first_page'].get('region',item['source']))
        item['region']          = get_region_name_id.get('get_region_id')              #省份id
        item['region_name']     = get_region_name_id.get('get_region_name')     #省份name
        item['shopnum']          = response.xpath('//div[@class="brandtxt"]//li[3]').xpath('string(.)').extract()[0].split('：')[-1:][0].replace('家','')
        item['trademark_cp']     = response.xpath('//div[@class="brandtxt"]//li[5]').xpath('string(.)').extract()[0].split('：')[-1:][0]
        item['trademark_throng'] = response.xpath('//div[@class="brandtxt"]//li[6]').xpath('string(.)').extract()[0].split('：')[-1:][0]
        item['pattern']          = ','.join(response.xpath('//div[@class="brandtxt"]//li[1]').xpath('string(.)').extract()[0].split('：')[-1:])
        item['content']          = ','.join(response.xpath('//div[@class="joincon"]').xpath('string(.)').extract())
        item['foundtime']        = response.xpath('//div[@class="groupbox"]/p[2]').xpath('string(.)').extract()[0].replace('成立时间：','')
        item['trademark_address']   = ','.join(response.xpath('//div[@class="groupbox"]/p[1]/text()').extract())
        item['slideshow']           = ','.join(response.xpath('//ul[@class="bigImg"]//li//img//@src').getall())
        item['feeid']               = item.alter_price(','.join(response.xpath('//div[@class="tztxtbox"]//b').xpath('string(.)').re('(\d+.*)万')))         #'5-10'
        item['process']             = ','.join(response.xpath('//div[@id="flow"]').xpath('string(.)').extract())
        item['advantage']           = response.xpath('//div[@id="youshi"]').xpath('string(.)').extract()
        fid_id_fid_name             =item.get_trademard_fid_id_fid_name(response.xpath('//dl[@class="location"]').xpath('string(.)').re('>(.*)')[0].replace('\r', '').split('>')[:2])
        item['fid']                 = fid_id_fid_name.get('fid_id')
        item['fid_name']            = fid_id_fid_name.get('fid_name')
        item['trademark_all_img']   = response.xpath('/html/body/div//img/@src').re('(.*.jpg)')
        item['thumb']               = response.xpath('//dt[@class="roundimgx"]/a/img/@src').get()             #招商列表轮播图
        item['title']               = ','.join(response.xpath('//div[@class="brandtxt"]//h3').xpath('string(.)').extract())
        item['companyname']         = response.xpath('//div[@class="groupbox"]/h6').xpath('string(.)').extract()[0]
        item['title_picture']       = ','.join(response.xpath('//dt[@class="roundimgx"]//img/@src').extract())
        # 会将ressponse插入mongo后，返回Mongo_id，插入到mysql中
        item['mongo_id']            = json.dumps(response.text)


        # for field in item.fields:
        #     if field in result_data.keys():
        #         item[field] = result_data.get(field)
        yield item









