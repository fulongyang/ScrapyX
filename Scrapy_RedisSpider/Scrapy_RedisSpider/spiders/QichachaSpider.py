# -*- coding: utf-8 -*-
import re
from collections import OrderedDict

import scrapy

from Scrapy_RedisSpider.items import CompanyItems, GetMysqlV3
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.spiders import CrawlSpider

class QichachaspiderSpider(GetMysqlV3,RedisSpider):
    name = 'QichachaSpider'
    # allowed_domains = ['m.qichacha.com']
    # start_urls = ['https://www.qichacha.com/search?key=鲁丽集团有限公司']
    # start_urls = ['https://m.qichacha.com/firm_069e80c5e6cd1d98fa0437ca5b302436.html']

    redis_key = 'QichachaSpider:QichachaSpiderQueue'


    # ----初始请求
    # def start_requests(self):
         # """Returns a batch of start requests from redis."""
        # yield scrapy.Request(url=self.start_urls[0],dont_filter=True)
    # def make_request_from_data(self, data):
    # def make_requests_from_url(self, url):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



    def parse(self, response):
        #--------------当请求链接是m端的时候，回调给解析函数
        if response.url.startswith('https://m.qichacha.com'):

            yield scrapy.Request(url=response.url,
                                 callback=self.parse_response_items,
                                 dont_filter=True,
                                 cookies={},
                                 headers={
                                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                                 },
                                 meta={'company_log':''})

        #-------------解析www端回调给解析函数
        search_items = response.xpath('//tbody[@id="search-result"]//tr')
        if search_items:
            try:
                for item in search_items:
                    link_tail = ''.join(item.xpath('td[3]/a/@href').get(default=''))
                    next_item_link = 'https://m.qichacha.com'+link_tail if link_tail else ''
                    company_log = re.findall('(.+?\.jpg|.+?\.png|.+?\.gif|.+?\.jpeg)',item.xpath('td[2]/img/@src').get(default=''))
                    # inspect_company = item.xpath('td[3]/a/@onclick').re("企业名称\'\:\'(.*?)\'\}")[0].replace('</em>','').replace('<em>','')

                    #---------------根据数据库去重
                    inspect_company = list(map(lambda x:x.replace('</em>','').replace('<em>',''),item.xpath('td[3]/a/@onclick').re("企业名称\'\:\'(.*?)\'\}")))
                    if inspect_company:
                        inspect_sql = "select Id,company_name from pp_company_info where company_name='{}' and spider_url='https://www.qichacha.com' limit 1;".format(inspect_company[0])
                        inspect_result = self.get_mysql_one(inspect_sql)
                        if inspect_result:
                            print('*' * 20, 'this company have in db ....', inspect_result.get('company_name', ''))
                            return
                    if link_tail:
                        #--请求m端不需要cookies
                        yield scrapy.Request(url=next_item_link,
                                             callback=self.parse_response_items,
                                             dont_filter=True,
                                             cookies={},
                                             headers={
                                            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                                            },
                                             meta={'company_log':company_log})
            except Exception as e:
                print(e)


    def parse_response_items(self,response):

        # 添加爬取网站
        #添加爬取当前页面
        # 添加主要成员
        # 添加主要企业状态
        # 修改mongo_id
        #todo 当错误的时候不妨碍字段输出设置
        if response.text.startswith('<script') or response.text.startswith('<!DOCTYPE html>')== False:

            yield scrapy.Request(url=response.url,
                                         callback=self.parse_response_items,
                                         dont_filter=True,
                                         cookies={},
                                         headers={
                                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                                        },
                                         meta={'company_log':response.meta.get('company_log','')})
            return

        #无固定期限 情况
        company_items = CompanyItems()
        company_info = OrderedDict()
        try:
            #----------------------企业信息
            company_info["company_log"] = response.meta.get('company_log','') #公司log图片
            company_info["company_name"] = response.xpath('//div[@class="company-name"]/text()').get(default='').replace('\n','')  # 企业名称
            if company_info['company_name']:
                print('company msg is False...')
                return
            company_info["company_legal_person"] = response.xpath('//div[@class="oper-warp"]/a/text()').get(default='').strip()  # 企业法人
            company_info["company_phone"] = response.xpath('//div[@class="contact-info-wrap"]/a/@href').re('(\d+)')  # 企业联系电话
            company_info["company_email"] = response.xpath('//div[@class="contact-info-wrap"]/a[2]/text()').get(default='')  # 企业邮箱
            company_info["company_address"] = response.xpath('//div[@class="address"]/text()').get(default='').strip()  # 企业地址
            company_info["company_code"] = response.xpath('//div[@class="basic-wrap"]/div[1]').xpath('string(.)').get(default='').strip().replace(' ', ':', 1).replace(' ', '').split(':')[-1:]  # 企业统一社会信用代码
            company_info["company_create_time"] = response.xpath('//div[@class="basic-wrap"]/div[4]').xpath('string(.)').get(default='').strip().replace(' ', ':', 1).replace(' ', '').split(':')[-1:]  # 企业成立日期
            company_info["company_type"] = response.xpath('//div[@class="basic-wrap"]/div[5]').xpath('string(.)').get(default='').strip().replace(' ', ':', 1).replace(' ', '').split(':')[-1:]  # 企业类型
            company_info["company_business_scope"] = response.xpath('//div[@class="basic-wrap"]/div[6]').xpath('string(.)').get(default='').strip().replace(' ', ':', 1).replace(' ', '')  # 企业经营范围
            company_info["company_capital"] = response.xpath('//div[@class="basic-wrap"]/div[3]').xpath('string(.)').get(default='').strip().replace(' ', ':', 1).replace(' ', '').split(':')[-1:]  # 认缴注册资本
            company_info["company_license_validity"] = response.xpath('//div[@class="basic-wrap"]/div[8]').xpath('string(.)').get(default='').strip().replace(' ', ':', 1).replace(' ', '').split(':')[-1:]  # 企业职照有效期
            company_info["company_contact"] = response.xpath('//div[@class="oper-warp"]/a/text()').get(default='').strip()  # 企业联系人
            company_info['company_status'] = response.xpath('//div[@class="basic-wrap"]/div[9]').xpath('string(.)').get(default='').strip().replace(' ', ':', 1).replace(' ', '').split(':')[-1:]  # 企业状态
            company_info['company_master'] = response.xpath('//div[@class="content-block"][3]/div[2]//div[@class="employee-name"]').xpath('string(.)').get(default='')  # 主要成员

            # company_info["company_license"] = response.xpath(" ")  # 企业执照
            # company_info["company_photo"] = response.xpath(" ")  # 企业图片
            # company_info["company_credentials"] = response.xpath(" ")  # 发证机关
            # company_info["company_contact_brand_all"] = response.xpath(" ")  # 企业关联品牌
            # company_info["company_qq"] = response.xpath(" ")  # 企业QQ
            # company_info["company_postcode"] = response.xpath(" ")  # 企业地区邮编
            # company_info["brand_name"] = response.xpath(" ")  # 品牌名称
            # company_info["company_credit"] = response.xpath(" ")  # 信用指数
            # company_info["company_license_permit_time"] = response.xpath(" ")  # 核准日期
            # company_info["company_contact_brand"] = response.xpath(" ")  # 企业关联品牌
            # company_info["company_web"] = response.xpath(" ")  # 企业官网
            # company_info["company_fax"] = response.xpath(" ")  # 企业传真
            # company_info["company_brand_honor"] = response.xpath(" ")  #企业品牌荣誉

            #--------------------固定内容--------------------------------------------
            # company_info["brand_partment_id"] = response.xpath(" ")  # 企业品牌外键
            # company_info["update_biaoshi"] = response.xpath(" ")  # 更新标识
            # company_info["update_time"] = response.xpath(" ")  # 最后更新时间
            # company_info["insert_time"] = response.xpath(" ")  # 插入时间
            # company_info["maigoo_company_mongo_id"] = response.xpath(" ")  # maigoo mongo_id
            company_info["mongo_id"] = response.text  # mongo_id
            company_info["mongo_url"] = response.url  # 当前爬取url
            company_info["spider_url"] = 'https://www.qichacha.com'  # 当前抓取网站区分url
            company_info = {k:''.join(v) if isinstance(v,list) else v for k,v in company_info.items()}
        except Exception as e:
            print(e)

        company_items.update(company_info)
        yield company_items







