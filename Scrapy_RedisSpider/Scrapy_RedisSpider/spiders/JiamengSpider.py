# -*- coding: utf-8 -*-
import random

import scrapy

from scrapy_redis.spiders import RedisSpider
from Scrapy_RedisSpider.items import ZhaoShanItem, get_trademard_fid_id_fid_name,get_region_name_id,alter_price


class JiamengspiderSpider(RedisSpider):
    name = 'JiamengSpider'
    allowed_domains = ['jiameng.com']
    start_urls = ['http://so.jiameng.com/bj/']

    redis_key = 'JiamengSpider:JiamengSpiderQueue'

    self_region_link = set()

    # def start_requests(self):
    #     """Returns a batch of start requests from redis."""
    #     yield scrapy.Request(url=self.start_urls[0],callback=self.parse,dont_filter=True,)


    def parse(self, response):

        #---------回调本页到解析函数
        items = response.xpath('//li[@class="items items_V clearfix"]')
        for item in items:
            # title = item.xpath('*/div[@class="bd-logo"]/a/img/@alt').extract()

            #----------company info
            # company_name = item.xpath('*//a[@class="text"]/@title').extract()
            # company_money = item.xpath('*//div[@class="showInfo"]/dl[2]').xpath('string(.)').extract()
            # item_vip_link = item.xpath('*/div[@class="bd-logo"]/a/@href').extract()
            company_create = item.xpath('*//div[@class="showInfo"]/dl[3]/dd/text()').re(r'(\d+\-\d+\-\d+)')
            company_address = item.xpath('*//div[@class="showInfo"]/dl[4]/dd/@title').extract()
            item_link = item.xpath('*/div[@class="text xijin"]/a[contains(text(),"图片")]/@href').extract()

            for next_item_link in item_link:
                next_item_url = next_item_link[:next_item_link.rindex('/')+1]
                yield scrapy.Request(url=next_item_url, callback=self.parse_item, dont_filter=False,
                                     meta={'company_create':company_create,'company_address':company_address})



        #-------------切换下一页
        
        detail_sum = response.xpath('//div[@class="fenPage"]/a[contains(text(),"下页")]/@href').extract()
        tail_link = 'http://so.jiameng.com' + detail_sum[0] if detail_sum else None
        if tail_link:
            yield scrapy.Request(url=tail_link, callback=self.parse, dont_filter=False,
                             meta={'region': '', 'up_response': ''})


        #--------------切换省份
        if len(self.self_region_link) <1:
            next_region = response.xpath('//dl[@id="zone-box"]//a[@class="filter_link"]/@href').extract()
            for region_link in next_region:
                self.self_region_link.add(region_link)
                yield scrapy.Request(url=region_link, callback=self.parse, dont_filter=False,
                                 meta={'region': '', 'up_response': ''})



    def parse_item(self,response):
        items = ZhaoShanItem()
        response_meta = response.meta
        #------------------------加盟
        items['spider_url'] = 'http://so.jiameng.com'  # 爬取网站
        items['contents'] = response.xpath('//div[@class="jm_xq_con"]').extract()  # 加盟详情全部
        items['content'] =   items['contents'][0]  # 加盟详情
        items['advantage'] = items['contents'][1]  # 加盟优势
        items['process'] =   items['contents'][2]  # 加盟流程
        #items['conditions'] = response.xpath()  # 加盟条件
        #items['analysis'] = response.xpath()  # 加盟分析
        items['manage'] = ','.join(response.xpath('//div[@class="jm_info"]//tr[3]/td[2]/text()').extract())  # 经营范围
        items['jiamengnum'] = random.randint(100,1000)  # 加盟人数
        feeid = response.xpath('//div[@class="jm_info"]//tr[8]/td[2]/text()').re(r'(\d+)') if response.xpath('//div[@class="jm_info"]//tr[8]/td[2]/text()').re(r'(\d+)') else response.xpath('//em[@class="jm-rmb-num"]/text()').get().split('~')  # 加盟价钱
        items['feeid'] =  alter_price(feeid)
        items['thumb'] = ','.join(response.xpath('//div[@class="holder"]/i/a/img/@src').extract())  # 轮播图
        items['title'] = response.xpath('//h2[@class="base_bd_title"]/@title').re(r'【(.*?)】')[0]  # 品牌名稱
        # items['update_biaoshi'] = response.xpath()  # 1:上传至oss
        fid_names = get_trademard_fid_id_fid_name(response.xpath('//div[@class="brand"]').xpath('string(.)').get().replace('\n','').split('>')[1:-1])  # 分类名称
        items['fid'] = fid_names.get('fid_id','')         #分类id
        items['fid_name'] = fid_names.get('fid_name','')  # 标签名
        items['trademark_throng'] = ','.join(response.xpath('//div[@class="jm_info"]//tr[3]/td[4]/text()').extract())  # 适合人群
        # items['async_part'] = response.xpath('//div[@class="w990"]/a[{}]/text() | //div[@class="w990"]/a[{}]/@href'.format(1,1)).extract()
        items['foundtime'] = ','.join(response_meta.get('company_create', '')) if response_meta.get('company_create', None) else ''.join(response.xpath('//div[@class="jm_info"]//tr[2]/td[2]/text()').extract())  # 品牌创立时间
        items['shopnum'] = ','.join(response.xpath('//div[@class="jm_info"]//tr[2]/td[4]/text()').extract())  # 门店总数
        items['slideshow'] = ','.join(response.xpath('//div[@class="comp_logo"]/img/@src').extract())  # 产品log图
        items['websiteurl'] = ','.join(response.xpath(
            '//li[@class="summary_site clear"]/div[@class="dd"]/span/text()').extract())  # 品牌官网网址
        # items['grade'] = response.xpath()  # 品牌评分
        # items['trademark_img'] = response.xpath()  # 品牌图片
        # items['trademark_cp'] = response.xpath()  # 品牌产品
        # items['title_picture'] = response.xpath()  # 品牌商标图片
        # items['pattern'] = response.xpath()  # 经营模式

        #---------------------公司
        items['companyname'] = ','.join(response.xpath('//div[@class="comp_info_con"]/h3/@title').extract())  # 公司名称
        items['source'] = ','.join(response.xpath('//div[@class="jm_info"]//tr[5]/td[2]/text()').extract())  # 品牌发源地/公司地址
        region = get_region_name_id(items['source'] if items['source'] else response.xpath('//div[@class="jm_info"]//tr[5]/td[2]/text()').extract())
        items['region'] =  region.get('get_region_id','')# 省份
        items['region_name'] = region.get('get_region_name','')  # 省份名
        # items['telephone'] = response.xpath()  # 固定电话
        # items['mobilephone'] = response.xpath()  # 移动手机
        # items['email'] = response.xpath()  # 邮箱地址
        # items['fax']   =   response.xpath()  # 公司传真
        # items['corporation'] = response.xpath()  # 公司法人
        # items['unite'] = response.xpath()  # 统一社会信用代码
        items['trademark_address'] =','.join(response.xpath('//div[@class="comp_info_con"]/ul/li[3]/em/text()').extract()) if 1 else  response_meta.get('company_address', '') # 公司地址

        #-----------------------其他
        items['trademark_all_img'] = ''  # 品牌所有图片
        items['mongo_id'] = response.text  # mongo id
        items['url'] = response.url  # 网站url
        return items






















