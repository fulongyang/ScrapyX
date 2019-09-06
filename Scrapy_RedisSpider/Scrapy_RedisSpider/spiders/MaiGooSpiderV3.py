# -*- coding: utf-8 -*-
import json
import random
import re
from urllib.parse import unquote
from scrapy_redis.spiders import RedisSpider
import scrapy

from Scrapy_RedisSpider.items import MaiGooItem, get_trademard_fid_id_fid_name, get_region_name_id, GetMysqlV3

start = '*' * 10
import pdb

'''
    1.修改只抓取排名
    

'''



class Maigoospiderv3Spider(RedisSpider):
    name = 'MaiGooSpiderV3'
    allowed_domains = ['maigoo.com']

    # start_urls      = ['https://www.maigoo.com/brand/search/?catid=7']
    redis_key = 'MaiGooSpiderV3:RequestQueueV3'

    next_linke = 'https://www.maigoo.com/ajaxstream/loadblock/?str=brand:search_BrandPY:,catid:{catid}-{classify}-0,num:10,page:{page}'
    search_link = 'https://www.maigoo.com/brand/search/?catid={catid}'

    comment_link = 'https://www.maigoo.com/ajaxstream/loadblock/?str=comment:commentlist_id:{comment_id},blockid:3,num:10,page:{page}'

    set_url = set()
    classify_dict = {'2729': '大品牌', '4636': '著名商标', '4635': '省市名牌', '2730': '驰名保护', '2731': '中华老字号', '4630': '高新技术企业',
                     '2732': '上市公司', '4813': '500强企业', '2733': '中小企业'}
    classify_dict_self = {'大品牌': '1', '省市名牌': '3', '驰名保护': '2', '高新技术企业': '5', '500强企业': '7', '中小企业': '8'}


    def parse(self, response):
        '''进入一级分类前'''

        # 第四大分类，与每个小分类进行组合
        # 'https://www.maigoo.com/ajaxstream/loadblock/?str=brand:search_BrandPY:,catid:1042-4636-0,num:10,page:1&append=0&t=1560927584017'
        # four_classify_num = response.xpath('//dl[@class="searchbrandlevel"]/dd/a/@value').getall()[1:]
        # for four_num in four_classify_num:
        #     classify = four_num

        # '一分类'
        first_classify_num = response.xpath('//dd/a[@level="secondcat"]/@value').extract()[:-1]
        first_classify_name = response.xpath('//dd/a[@level="secondcat"]/text()').extract()[:-1]

        # --------------------收集一类分类
        first_classify_dict = dict(zip(first_classify_num,first_classify_name))
        self.classify_dict.update(first_classify_dict)

        for first_num in first_classify_num:
            # --------------------------start
            first_search_link = self.search_link.format(catid=first_num)

            # '横向  切换下一页'
            first_next_link = self.next_linke.format(catid=first_num, classify=0, page=1)
            if first_next_link not in self.set_url:
                self.set_url.add(first_next_link)
                yield scrapy.Request(url=first_next_link, callback=self.next_page, dont_filter=True,
                                     meta={'classify_name': '', 'catid': first_num, 'classify_id': 0, })

            if first_search_link not in self.set_url:
                self.set_url.add(first_search_link)
                # '横向  切换下一 1分类，回调给自己,https://www.maigoo.com/brand/search/?catid=1'
                yield scrapy.Request(url=first_search_link, callback=self.parse, dont_filter=False,
                                     # meta={'classify': classify_dict[brandlevel], 'catid': first_num,'classify_id': classify_id, }
                                     )

            # --------------------------------end

        # --------------------------------start  todo 暂停
        # '二分类  2分类，   注意：二分类中存在三分类'
        two_classify_num = response.xpath('//dl[@class="category secondcat"]/dd/a/@value').getall()[1:]
        two_classify_name = response.xpath('//dl[@class="category secondcat"]/dd/a/text()').getall()[1:]

        #--------------------收集二类分类
        two_classify_dict = dict(zip(two_classify_num, two_classify_name))
        self.classify_dict.update(two_classify_dict)

        for two_num in two_classify_num[1:]:
            tow_link = self.search_link.format(catid=two_num)
            # '链接去重'
            if tow_link not in self.set_url:
                self.set_url.add(tow_link)

                # '纵向 切换下一2分类， 回调给自己,https://www.maigoo.com/brand/search/?catid=57'
                yield scrapy.Request(url=tow_link, callback=self.parse, dont_filter=False,
                                     meta={'catid': two_num, 'classify_name': '', 'classify_id': 0, }
                                     )

            # '纵向 切换下一2分类， 回调给下一页,'
            tow_next_link = self.next_linke.format(catid=two_num, classify=0, page=1)
            if tow_next_link not in self.set_url:
                self.set_url.add(tow_next_link)
                yield scrapy.Request(url=tow_next_link, callback=self.next_page, dont_filter=False,
                                     meta={'catid': two_num, 'classify_name': '', 'classify_id': 0, })

        # --------------------------------end

        # --------------------------------start
        # '三分类  二分类中的三分类.没进入二分类,不存在这个分类需要判断是否解析到结果'
        three_classify = response.xpath('//dl[@class="category thirdcat"]/dd/a/@value').getall()
        three_classify_name = response.xpath('//dl[@class="category thirdcat"]/dd/a/text()').getall()
        if three_classify:
            #----------------------收集三类分类
            three_classify_dict = dict(zip(three_classify, three_classify_name))
            self.classify_dict.update(three_classify_dict)

            for three_num in three_classify[1:]:
                three_link = self.search_link.format(catid=three_num)
                # '链接去重'
                if three_link not in self.set_url:
                    self.set_url.add(three_link)

                    # '横向 切换三分类下一分类  回调给自己'
                    yield scrapy.Request(url=three_link, callback=self.parse, dont_filter=False,
                                         # meta={'classify': classify_dict[brandlevel], 'catid': catid,'classify_id': classify_id,}
                                         )

                # '横向 切换三分类下一分类  回调给解析函数'
                three_next_link = self.next_linke.format(catid=three_num, classify=0, page=1)
                if three_next_link not in self.set_url:
                    self.set_url.add(three_next_link)
                    yield scrapy.Request(url=three_next_link, callback=self.next_page, dont_filter=False,
                                         meta={'classify_name':0, 'catid': three_num, 'classify_id': 0, })

        # --------------------------------end
    def next_page(self, response):
        '''递归翻页'''
        index = response.xpath('//div[@class="num"]/text()').getall()

        classify_id = response.meta.get('classify_id')
        catid = response.meta.get('catid')
        # '''递归翻页'''
        page = re.findall('page:(\d+)', response.url)
        if index and page:
            page = int(page[0]) + 1 if int(page[0]) < 50 else None
            next_page = self.next_linke.format(catid=catid, classify=classify_id, page=page)
            if next_page not in self.set_url:
                self.set_url.add(next_page)
                yield scrapy.Request(url=next_page,
                                     callback=self.next_page, dont_filter=False,
                                     meta={'catid': catid,
                                           'classify_id': classify_id})
        # '''解析品牌，回调给字段函数'''

        # https://www.maigoo.com/ajaxstream/loadblock/?str=brand:search_BrandPY:,q:,catid:2990--4636,num:10,page:8&append=1&t=1560239348974
        more_next_pp_links = response.xpath('//a[@class="c3f6799 b"]/@href').getall()
        titles = response.xpath('//a[@class="c3f6799 b"]/text()').getall()
        index = response.xpath('//div[@class="num"]/text()').getall()
        for item_index, more_next_pp_link, titlea in zip(index, more_next_pp_links, titles):

            title = titlea.replace('"','').replace("'","")
            

            print(item_index)
            print(start, item_index, start)
            if more_next_pp_link not in self.set_url:
                self.set_url.add(more_next_pp_link)
                # ------------------mysql 去重  根据分类名称 和title进行去重
                classify_names = re.findall('catid:(\d+)', response.url)[0]
                classify_name = self.classify_dict.get(classify_names,'None').replace('"','').replace("'","")
                
                get_mysql = GetMysqlV3()
                if get_mysql.get_one('title', title,classify_name):
                    get_mysql.update_id(classify_name, title)
                    print(start, title, 'is in mysql', start)
                    continue
                get_mysql.close_mysql()
                print(self.classify_dict)
                print(start, title,classify_name, 'not in  mysql', start)
                # ------------------mysql 去重 end


                yield scrapy.Request(url=more_next_pp_link, callback=self.parse_response_item, dont_filter=False,
                                     meta={'index_item': item_index, 'classify_id': classify_id,'classify_name':classify_name})


    def parse_response_item(self, response):
        '''解析需要数据'''
        items = MaiGooItem()
        try:
            fid_id_fid_name = get_trademard_fid_id_fid_name(
                response.xpath('//div[@class="position"]/a').xpath('string(.)').getall()[1:3])
            items['fid'] = fid_id_fid_name.get('fid_id')  # 行业分类ID
            items['scope'] = fid_id_fid_name.get('fid_name')  # 行业分类名稱
            items['title'] = response.xpath('//span[@class="font22 line18em b"]').xpath('string(.)').get()  # 标题
            items['thumb'] = response.xpath('//div[@class="img"]/a/img/@src').get()  # 缩略图
            items['address'] = response.xpath('//li[@class="dhidden"]/span[1]/text()').get().split('：')[1]  # 品牌发源地
            get_region = get_region_name_id(
                key=response.xpath('//li[@class="dhidden"]/span[1]/text()').get().split('：')[1][:2])
            items['region'] = get_region.get('get_region_id')  # 省份id
            region_name = get_region.get('get_region_name')  # 省份
            items['foundtime'] = response.xpath('//li[@class="dhidden"]/span[2]/text()').get().split('：')[1]  # 品牌创立时间
            items['corporation'] = response.xpath('//span[@class="mgl"]/a/text()').get()  # 公司法人
            items['telphone'] = ','.join(response.xpath('//div[@class="info"]').re('i>(.*?)</span'))  # 固话
            company_name = response.xpath('//a[@class="font16"]').xpath('string(.)').get()
            items['companyname'] = company_name.replace('（', '').replace('）',
                                                                         '') if company_name else company_name  # 公司名称
            items['websiteurl'] = unquote(response.xpath('//div[@class="img"]/a/@href').get().split('=')[1])  # 官网
            items['content'] = response.xpath('//div[@class="desc"]').get()  # 内容
            items['slideshow'] = ','.join(response.xpath('//div[@class="img big"]/img/@src').getall())  # 轮播图
            items['bid'] = self.classify_dict_self.get(
                self.classify_dict.get(response.meta.get('classify_id', 'None')))  # 品牌等级
            items['bid_name'] = self.classify_dict.get(response.meta.get('classify_id', 'None'))  # 品牌等级名稱
            items['grade'] = random.randint(1, 5)  # 品牌评分（1-5随机）
            items['email'] = response.xpath('//i[contains(@class,"icon-email")]/@ptitle').get()

            # self link
            items['corporation_link'] = response.xpath('//span[@class="mgl"]/a/@href').get()  # 公司法人_link
            items['websiteurl_info'] = response.xpath('//a[@class="font16"]/@href').get()
            items['mongo_id'] = json.dumps(response.text)
            items['url'] = response.url
            items['index_item'] = response.meta.get('index_item', '')
            items['classify_name'] = response.meta.get('classify_name', '')
            items['user_comment'] = []
            
            yield items
            
            # 评论
            # comment_id = response.xpath('//div[@class="brandud"]/@brandid').get()
            # 
            # yield scrapy.Request(url=self.comment_link.format(comment_id=comment_id, page=1),
            #                      callback=self.parse_item_comment,
            #                      dont_filter=False, meta={'pp_items': items, 'comment_id': comment_id, })
        except Exception as e:
            print(e)



    def parse_item_comment(self, response):
        '''解析评论，递归回调下一页'''
        pp_items = response.meta['pp_items']
        comment_id = response.meta['comment_id']
        # user_comment = response.xpath('//div[@class="usersay"]').getall()      #全部原始數據
        # parse_comment = response.xpath('//div[contains(@class,"commenttxt line15em")] | //div[contains(@class,"commenttime font12")]').extract()
        user_comment = list(
            map(str.strip, response.xpath('//div[contains(@class,"usersay")]').xpath('string(.)').extract()))
        user_comment_copy = user_comment.copy()
        pp_items['user_comment'] += user_comment
        page = int(re.findall('page.*(\d+)', response.url)[0]) + 1 if user_comment_copy else None
        # '如果存在下一页  就翻页   直到没有下一页  返回所有items'
        if page:
            comment_next_url = self.comment_link.format(comment_id=comment_id, page=page)
            # print(pp_items['user_comment'])
            print(comment_next_url)
            print(start * 5)
            yield scrapy.Request(url=comment_next_url, callback=self.parse_item_comment, dont_filter=False,
                                 meta={'pp_items': pp_items, 'comment_id': comment_id, }
                                 )
        else:
            yield pp_items























