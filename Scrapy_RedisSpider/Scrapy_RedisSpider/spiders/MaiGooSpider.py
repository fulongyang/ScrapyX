# -*- coding: utf-8 -*-
import json
import random
import re

import scrapy
from scrapy_redis.spiders import RedisSpider

from scrapy.loader import ItemLoader
from Scrapy_RedisSpider.items import MaiGooItem


from Scrapy_RedisSpider.items import get_trademard_fid_id_fid_name,get_region_name_id

from urllib.parse import unquote

from helper import UploadOSS

set_url = {}
import threading

# class MaigoospiderSpider(UploadOSS,scrapy.Spider):
class MaigoospiderSpider(UploadOSS,RedisSpider):
    name = 'MaiGooSpider'
    allowed_domains = ['maigoo.com']


    #----------单机模式  or 分布式模式
    scrapy_model = 'RedisSpider'
    if scrapy_model == 'Spider':                #选择爬虫模式
        start_urls = ['https://www.maigoo.com/brand/search/?catid=7&brandlevel=2729']
    elif scrapy_model == 'RedisSpider':
        redis_key = 'MaiGooSpider:RequestQueue'
    set_url = set()


    def classify_parse(self,response):
        # 找到当前品牌属于哪个分类
        classify = response.xpath('//dl[@class="searchbrandlevel"]/dd/a/@value').getall()[1:]
        classify_txt = response.xpath('//dl[@class="searchbrandlevel"]/dd/a/text()').getall()[1:]
        classify_dict = dict(zip(classify, classify_txt))
        brandlevel = re.findall('brandlevel=(\d+)', response.url)[0]
        return classify_dict


    def parse(self, response):
        # 找到当前品牌属于哪个分类
        classify_dict = self.classify_parse(response)
        brandlevel = re.findall('brandlevel=(\d+)', response.url)[0]

        #解析一类分类，回调给下一页
        next_linke = 'https://www.maigoo.com/ajaxstream/loadblock/?str=brand:search_BrandPY:,catid:{catid}-{classify}-0,num:10,page:{page}'
        first_ids = response.xpath('//dd/a[@level="secondcat"]/@value').extract()[:-1]
        classify_ids = response.xpath('//dl[@class="searchbrandlevel"]/dd/a/@value').getall()[1:]



        for catid in first_ids:
            for classify_id in classify_ids:
                url = next_linke.format(catid=catid, classify=classify_id, page=1)
                if url not in self.set_url:
                    self.set_url.add(url)
                    yield scrapy.Request(url=url,callback=self.parse_next_more_page, dont_filter=True,meta={'classify':classify_dict[brandlevel],'catid':catid,'classify_id':classify_id})



        #进入品牌页面链接  回调给解析函数
        next_pp_links = response.xpath('//div[@class="resultleft"]/a/@href').extract()
        next_pp_imgs = response.xpath('//div[@class="resultleft"]/a//img/@data-src').extract()   #品牌图片
        phone = response.xpath('//div[contains(@phone,"-")]/@phone').getall()   #电话
        for next_pp_link in next_pp_links:
            yield scrapy.Request(url=next_pp_link, callback=self.parse_navigation_response, dont_filter=True,
                                 meta={'classify':classify_dict[brandlevel],})



        #解析一类品牌+品牌分类给下一页
        # next_linke = 'https://www.maigoo.com/ajaxstream/loadblock/?str=brand:search_BrandPY:,catid:{catid}-{classify}-0,num:10,page:{page}'
        # catid = re.findall('catid=(\d+)', response.url)[0]
        # brandlevel = re.findall('brandlevel=(\d+)', response.url)[0]
        # yield scrapy.Request(url=next_linke.format(catid=catid,classify=brandlevel,page=2), callback=self.parse_next_more_page, dont_filter=True,
        #                      meta={'parse_meta':''})
        #


    def parse_next_more_page(self,response):


        #递归回调给自己
        next_linke = 'https://www.maigoo.com/ajaxstream/loadblock/?str=brand:search_BrandPY:,catid:{catid}-{classify}-0,num:10,page:{page}'
        #--------
        # catid = re.findall('catid=(\d+)', response.url)[0]
        # brandlevel = re.findall('brandlevel=(\d+)', response.url)[0]

        classify_id = response.meta.get('classify_id')
        catid = response.meta.get('catid')

        more_id =response.xpath('//div[@class="num"]/text()').getall()
        max_id = max(more_id) if more_id else 0

        #需要解决这个到达50页会怎么样
        page = int(re.findall('page:(\d+)', response.url)[0])
        page = page+1 if page<50 else None
        if page:
            next_page = next_linke.format(catid=catid, classify=classify_id, page=page)
            if next_page not in self.set_url:
                yield scrapy.Request(url=next_page,
                                     callback=self.parse_next_more_page, dont_filter=True,
                                     meta={'classify':response.meta.get('classify'),'catid':catid,'classify_id':classify_id})


        '''解析品牌，回调给字段函数'''
        # https://www.maigoo.com/ajaxstream/loadblock/?str=brand:search_BrandPY:,q:,catid:2990--4636,num:10,page:8&append=1&t=1560239348974
        more_next_pp_links = response.xpath('//a[@class="c3f6799 b"]/@href').getall()
        for more_next_pp_link in more_next_pp_links:
            yield scrapy.Request(url=more_next_pp_link, callback=self.parse_navigation_response, dont_filter=True,
                                 meta={'classify':response.meta.get('classify')})


    def parse_navigation_response(self, response):
        #-----------ItemLoader
        #------------测试利用继承类上传oss
        # slideshow = super().upload_oss(response.xpath('//div[@class="img big"]/img/@src').get())
        # ---------------item
        items = MaiGooItem()
        fid_id_fid_name      =get_trademard_fid_id_fid_name(response.xpath('//div[@class="position"]/a').xpath('string(.)').getall()[1:3])
        items['fid']         = fid_id_fid_name.get('fid_id')        # 行业分类ID
        fid_name             = fid_id_fid_name.get('fid_name')        # 行业分类ID
        items['title']       = response.xpath('//span[@class="font22 line18em b"]').xpath('string(.)').get()  # 标题
        items['thumb']       = response.xpath('//div[@class="img"]/a/img/@src').get()  # 缩略图
        items['address']     = response.xpath('//li[@class="dhidden"]/span[1]/text()').get().split('：')[1]  # 品牌发源地
        get_region           = get_region_name_id(key=response.xpath('//li[@class="dhidden"]/span[1]/text()').get().split('：')[1][:2])
        items['region']      = get_region.get('get_region_id')      # 省份id
        region_name          = get_region.get('get_region_name')    # 省份
        items['foundtime']   = response.xpath('//li[@class="dhidden"]/span[2]/text()').get().split('：')[1]  # 品牌创立时间
        items['corporation'] = response.xpath('//span[@class="mgl"]/a/text()').get()  # 公司法人
        items['telphone']    = ','.join(response.xpath('//div[@class="info"]').re('i>(.*?)</span'))  # 固话
        items['companyname'] = response.xpath('//a[@class="font16"]').xpath('string(.)').get().replace('（','').replace('）','')  # 公司名称
        items['websiteurl']  = unquote(response.xpath('//div[@class="img"]/a/@href').get().split('=')[1])  # 官网

        items['content']     = response.xpath('//div[@class="desc"]').get()  # 内容
        items['slideshow']   = response.xpath('//div[@class="img big"]/img/@src').get()  # 轮播图
        items['bid']         = response.meta.get('classify','None')  # 品牌等级（500强。。。）
        items['grade']       = random.randint(1,5)  # 品牌评分（1-5随机）
        items['company_email'] = response.xpath('//i[contains(@class,"icon-email")]/@ptitle').get()
        items['mongo_id']         = json.dumps(response.text)

        #self link
        items['corporation_link'] = response.xpath('//span[@class="mgl"]/a/@href').get()  # 公司法人_link
        items['websiteurl_info']  = response.xpath('//a[@class="font16"]/@href').get()
        items['url']         =response.url

        return items











