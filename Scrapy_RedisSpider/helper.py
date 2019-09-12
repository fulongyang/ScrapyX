import base64
import json

import pymysql
import requests
from pymysql import IntegrityError
from scrapy.utils.project import get_project_settings
setting = get_project_settings()




#------------获取解析规则
class GetParseRule():


    def get_mysql_rule(self,conn):
        cursor = conn.cursor()
        get_rule_sql = "select * from PlutonianRule order by id desc;"
        result_rule_sql = cursor.execute(get_rule_sql).fetchall()
        yield from result_rule_sql






class GetAPIProxy():
    '''接口获取代理
        参考 :https://github.com/fulongyang/proxy_pool
    '''
    @classmethod
    def get_proxy(cls,url):
        '''获取代理ip'''
        return requests.get(url).json()

    @classmethod
    def delete_proxy(cls,url,proxy):
        '''删除代理ip'''
        requests.get(url.format(proxy))



class ABYProxy():
    
    @classmethod
    def set_RandomProxyMiddleware(cls,request,spider):
        proxyHost = setting['ABY_PROXY_HOST']
        proxyPort = setting['ABY_PROXY_PORT']
        proxyUser = setting['ABY_PROXY_USER']
        proxyPass = setting['ABY_PROXY_PASS']
        proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
        request.meta["proxy"] = 'http://' + proxyHost + ':' + proxyPort
        request.headers["Proxy-Authorization"] = proxyAuth
        # request.headers["Proxy-Switch-Ip"] = 'yes'
        print('*' * 20, '使用阿布云代理', request.meta['proxy'])





class UploadOSS():

    def __init__(self):
        self.start = '*'*20



