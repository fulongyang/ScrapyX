# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import asyncio
import base64
import hashlib
import json
import random
import time

import pymysql
import redis
import requests
from scrapy import signals, log
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from pyppeteer import launch
import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import IgnoreRequest

from scrapy.utils.log import configure_logging
from scrapy.utils.response import response_status_message
from twisted.enterprise import adbapi
from Scrapy_RedisSpider.items import GetMysqlV3
from scrapy.utils.project import get_project_settings

from helper import GetAPIProxy, ABYProxy

setting = get_project_settings()
star = '*' * 20

#--------------------cookieMiddleword


class CookieMiddleware(RetryMiddleware):
    


    def process_request(self, request, spider):

        #----------------cookie代理设置
        Cookie = [{'Cookie':'UM_distinctid=16b07a5410188e-0370fbffdd06af-e353165-1fa400-16b07a54102adc; zg_did=%7B%22did%22%3A%20%2216b07a54a2ab69-020cbf4311ac2d-e353165-1fa400-16b07a54a2ba8a%22%7D; QCCSESSID=v0k6bn3k9kdo2m43o78k9pd201; acw_tc=2ff61d9615652582495268893eace9c1cab8eccddbee323e516e0182f2; PHPSESSID=p9kao4cvmlu55gcjetsg8t6vo0; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1565258235,1565260494; CNZZDATA1254842228=202906615-1565256669-%7C1566444601; acw_sc__v2=5d5e0cd1f204ec2a03de1a30e76278aca77703c9; acw_sc__v3=5d5e0cd8c1eff23b973d800ad43bc08d6db14c80; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201566442757382%2C%22updated%22%3A%201566445150276%2C%22info%22%3A%201565866180432%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1566445150'}
                  ]
        request.cookies = random.choices(Cookie)[0]
        return None


    def process_response(self, request, response, spider):
        # 携带cookie进行页面请求时，可能会出现cookies失效的情况。访问失败会出现两种情况：1. 重定向302到登录页面；2. 也能会出现验证的情况；

        # 想拦截重定向请求，需要在settings中配置。
        if response.status in [405, 404]:
            # 如果出现了重定向，获取重定向的地址
            redirect_url = response.headers
            if 'passport' in redirect_url:
                # 重定向到了登录页面，Cookie失效。
                # self.logging.info('Cookies Invaild!')
                pass
            if '验证页面' in redirect_url:
                # Cookies还能继续使用，针对账号进行的反爬虫。
                # self.logging.info('当前Cookie无法使用，需要认证。')
                pass
            # 如果出现重定向，说明此次请求失败，继续获取一个新的Cookie，重新对此次请求request进行访问。
            # 返回值request: 停止后续的response中间件，而是将request重新放入调度器的队列中重新请求。
            
        print(star,response.status)
        if self.inspect_startcontext(response.text):
            log.msg('*'*10+'没有拿到正确页面', level=log.INFO)
            #----------重试请求
            retry_req = request.copy()
            retry_req.dont_filter = True  # 必须设置(禁止重复请求被过滤掉)
            retry_req.priority = request.priority + self.priority_adjust
            return retry_req or response
        # 如果没有出现重定向，直接将response向下传递后续的中间件。
        return response


    def inspect_startcontext(self, context):
        '检测内容是否正确'
        if context.startswith('<script'):
            return True
        else:
            return False

    def process_response_test(self, request, response, spider):

        # 携带cookie进行页面请求时，可能会出现cookies失效的情况。访问失败会出现两种情况：1. 重定向302到登录页面；2. 也能会出现验证的情况；
        # 想拦截重定向请求，需要在settings中配置。
        if response.status in [302, 301]:
            # 如果出现了重定向，获取重定向的地址
            redirect_url = response.headers['location']
            if 'passport' in redirect_url:
                # 重定向到了登录页面，Cookie失效。
                self.logging.info('Cookies Invaild!')
            if '验证页面' in redirect_url:
                # Cookies还能继续使用，针对账号进行的反爬虫。
                self.logging.info('当前Cookie无法使用，需要认证。')

            # 如果出现重定向，说明此次请求失败，继续获取一个新的Cookie，重新对此次请求request进行访问。
            request.cookies = self.get_random_cookies()
            # 返回值request: 停止后续的response中间件，而是将request重新放入调度器的队列中重新请求。
            return request

        # 如果没有出现重定向，直接将response向下传递后续的中间件。
        return response

    def get_random_cookies(self):
        '''获取cookies函数'''
        try:
            response = requests.get(self.cookies_pool_url)
        except Exception as e:
            self.logging.info('Get Cookies failed: {}'.format(e))
        else:
            # 在中间件中，设置请求头携带的Cookies值，必须是一个字典，不能直接设置字符串。
            cookies = json.loads(response.text)
            self.logging.info('Get Cookies success: {}'.format(response.text))
            return cookies



async def get_web_cookie(url):
    '''获取文本信息'''

    browser = await launch({'headless': False, 'args': ['--no-sandbox'
                                                        ,'--proxy-server=112.111.199.104:4261'], })  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()
    # --------------处理浏览器识别
    # await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    #  window.navigator.webdriver

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')
    res = await page.goto(url)
    resp_status = res.status  # 响应状态
    # conetnt_txt = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    print(cookies)
    await page.waitFor(5)
    await page.close()
    # 等待
    await asyncio.sleep(5)
    return cookies



#--------请求头
class RandomUserAgent(GetMysqlV3,UserAgentMiddleware):

    def __init__(self,user_agent,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.user_agent = user_agent

    def process_request(self, request, spider):

        # --------根据数据库去重
        from urllib.parse import unquote
        url_link = unquote(request.url)
        _company_name = url_link.split('=')[-1:][0]
        inspect_sql = "select Id,company_name from pp_company_info where company_name='{}' limit 1;".format(
            _company_name)
        inspect_result = self.get_mysql_one(inspect_sql)
        if inspect_result:
            print('*' * 20, 'this company have in db ....', inspect_result.get('company_name', ''))
            raise IgnoreRequest


        #从列表中随机抽选出一个ua值
        ua = random.choice(user_agent_list)
        log.msg(request.url+'\nCurrent UserAgent: ' + ua, level=log.INFO)
        #ua值进行当前拦截到请求的ua的写入操作
        request.headers.setdefault('User-Agent',ua)
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass


from twisted.internet import defer
from twisted.internet.error import *
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from urllib.parse import unquote
from twisted.internet.error import TimeoutError
# ---------------代理ip
class RandomProxyMiddleware(RetryMiddleware):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)


    def process_request(self, request, spider):
        url_link = unquote(request.url)
        print(star, '代理', url_link,request.headers)

        if spider.name == 'QichachaSpider':
            #-------------拒绝处理请求
            if '公司' not in url_link and request.url.startswith('https://www.qichacha.com'):
                print('*'*20,'company name not in url link...',url_link)
                raise IgnoreRequest


        select_proxy =random.randint(1,2)
        #使用阿布云代理
        if setting['ABY_PROXY_USER']:
            ABYProxy.set_RandomProxyMiddleware(request,spider)

        #-------------使用接口代理
        elif setting['QICHACHA_GET_IP_URL']:
            proxy_pool_ip = GetAPIProxy.get_proxy().get('proxy')
            request.meta['proxy'] = 'http://{}'.format(proxy_pool_ip)
            print('*' * 20, '使用proxyPool',request.meta['proxy'])
        elif select_proxy:
            url = 'http://proxy.1again.cc:35050/api/v1/proxy/?https=1'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36', }
            github_proxy_ip = requests.get(url, verify=False, headers=headers).json().get('data', {}).get('proxy')
            request.meta['proxy'] = 'http://{}'.format(github_proxy_ip)
            print('*' * 20, '使用GithubProxy', request.meta['proxy'])
        return None


    def process_response(self, request, response, spider):
        try_code = 0
        if spider.name == 'QichachaSpider':
            if response.status in [405, 404]:
                # 如果出现了重定向，获取重定向的地址
                redirect_url = response.headers
                if 'passport' in redirect_url:
                    # 重定向到了登录页面，Cookie失效。
                    # self.logging.info('Cookies Invaild!')
                    pass
                if '验证页面' in redirect_url:
                    # Cookies还能继续使用，针对账号进行的反爬虫。
                    # self.logging.info('当前Cookie无法使用，需要认证。')
                    pass
                try_code = 1

            #没有拿到正确页面重试
            if self.inspect_startcontext(response.text):
                log.msg('*'*10+'no take right page try again ', level=log.INFO)
                #------------打印出失败的ip删除
                find_proxy_ip = request.meta['proxy'][7:]
                GetAPIProxy().delete_proxy(find_proxy_ip)
                print('*'*20,'delete ip ok',find_proxy_ip)
                try_code = 1

            #内容不正确重试
            if response.url.startswith('https://m.qichacha.com'):
                company_name = response.xpath('//div[@class="company-name"]/text()').get(default='').replace('\n','')
                if company_name =='':
                    try_code =1
                    print('*'*20,'page info is error try agent',company_name)

            if response.url.startswith('https://www.qichacha.com'):
                if  '没找到数据' in response.text:
                    try_code = 0

        #启动重试机制
        if try_code ==1:
            retry_req = request.copy()
            retry_req.dont_filter = True  # 必须设置(禁止重复请求被过滤掉)
            retry_req.priority = request.priority + self.priority_adjust
            return retry_req or response
        # 如果没有出现重定向，直接将response向下传递后续的中间件。
        return response


    def inspect_startcontext(self,context):
        '检测内容是否正确'
        if context.startswith('<script'):
            return True
        else:
            return False


    def process_exception(self, request, exception, spider):

        try_code = 0
        #---------请求超时错误  重试
        if isinstance(exception, TimeoutError):
            try_code = 1

        # ------------打印出失败的ip删除
        if exception.args  and 'Could not open ' in exception.args[0]:
            print('*'*20,'error',exception.args[0])
            find_proxy_ip = request.meta['proxy'][7:]
            GetAPIProxy().delete_proxy(find_proxy_ip)
            print('*' * 20, 'delete ip ok', find_proxy_ip)
            try_code = 1

        if exception.args and 'have in db' in exception.args[0]:
            print('*'*20,exception)
            pass

        if try_code ==1:
            # ----------重试二  成功持续重试
            retry_req = request.copy()
            retry_req.dont_filter = True  # 必须设置(禁止重复请求被过滤掉)
            retry_req.priority = request.priority + self.priority_adjust
            print('*' * 20, 'process_exception try agent  ok')
            return retry_req


class PpRedisspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PpRedisspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


user_agent_list_phone = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
]


user_agent_list = [
        'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,likeGecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html）',
        'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 likeMac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143Safari/601.1 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',

]






if __name__ == "__main__":
    url = 'https://www.qichacha.com'
    coo = asyncio.get_event_loop().run_until_complete(get_web_cookie(url))
