# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import json
import random

import pymysql
import scrapy
from scrapy.utils.project import get_project_settings
setting = get_project_settings()
start = '*'*15
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import TakeFirst,Join


#---------------------企业信息
class CompanyItems(scrapy.Item):
    # Dynamic_assignment = {
    #     "company_code": "企业统一社会信用代码",
    #     "company_license": "企业执照",
    #     "brand_partment_id": "企业品牌外键",
    #     "maigoo_company_mongo_id": "maigoo mongo_id",
    #     "update_biaoshi": "更新标识",
    #     "company_photo": "企业图片",
    #     "company_name": "企业名称",
    #     "company_credentials": "发证机关",
    #     "company_contact_brand_all": "企业关联品牌_html",
    #     "company_email": "企业邮箱",
    #     "company_phone": "企业联系电话",
    #     "company_qq": "企业QQ",
    #     "company_legal_person": "企业法人",
    #     "company_postcode": "企业地区邮编",
    #     "company_capital": "认缴注册资本",
    #     "company_address": "企业地址",
    #     "company_license_validity": "企业职照有效期",
    #     "brand_name": "品牌名称",
    #     "company_create_time": "企业成立日期",
    #     "company_credit": "信用指数",
    #     "company_license_permit_time": "核准日期",
    #     "company_contact": "企业联系人",
    #     "company_contact_brand": "企业关联品牌",
    #     "company_type": "企业类型",
    #     "update_time": "最后更新时间",
    #     "company_web": "企业官网",
    #     "insert_time": "插入时间",
    #     "company_fax": "企业传真",
    #     "company_business_scope": "企业经营范围",
    #     "company_brand_honor": "企业品牌荣誉",
    #     "mongo_id": "mongo_id",
    #     "mongo_url": "爬取网站url",
    #     "spider_url": "当前抓取网站区分url",
    #     "company_status": "企业状态",
    #     "company_master": "公司主要成员",
    #     }
    # 
    
    Dynamic_assignment = {'company_name': ' 企业名称',
     'company_legal_person': ' 企业法人',
     'company_phone': ' 企业联系电话',
     'company_email': ' 企业邮箱',
     'company_address': ' 企业地址',
     'company_code': ' 企业统一社会信用代码',
     'company_create_time': ' 企业成立日期',
     'company_type': ' 企业类型',
     'company_business_scope': ' 企业经营范围',
     'company_capital': ' 认缴注册资本',
     'company_license_validity': ' 企业职照有效期',
     'company_contact': ' 企业联系人',
     'company_status': ' 企业状态',
     'company_master': ' 主要成员',
     'company_license': ' 企业执照',
     'company_photo': ' 企业图片',
     'company_credentials': ' 发证机关',
     'company_contact_brand_all': ' 企业关联品牌',
     'company_qq': ' 企业QQ',
     'company_postcode': ' 企业地区邮编',
     'brand_name': ' 品牌名称',
     'company_credit': ' 信用指数',
     'company_license_permit_time': ' 核准日期',
     'company_contact_brand': ' 企业关联品牌',
     'company_web': ' 企业官网',
     'company_fax': ' 企业传真',
     'company_brand_honor': ' 企业品牌荣誉',
     'company_log': ' 企业Log图',

    #---------------默认参数
     'brand_partment_id': ' 企业品牌外键',
     'maigoo_company_mongo_id': ' maigoo mongo_id',
     'update_biaoshi': ' 更新标识',
     'update_time': ' 最后更新时间',
     'insert_time': ' 插入时间',
     'mongo_id': ' mongo_id',
     'mongo_url': ' 当前爬取url',
     'spider_url': ' 当前抓取网站区分url',
                          }
    


    #----------动态赋值2   实现成功
    for k,v in Dynamic_assignment.items():
        locals()[k] = scrapy.Field()



    

#----------------------招商字段
class ZhaoShanItem(scrapy.Item):

    zhaoshang_dict_word01 = {
        'title':'品牌名稱',
        'spider_url':'爬取网站',
        'region':'省份',
        'region_name':'省份名',
        'companyname':'公司名称',
        'fid_name':'分类名称',
        'fid':'	分类id',
        'source':'公司地址',
        'contents':'招商全部',
        'content':'加盟详情',
        'manage':'经营范围',
        'foundtime':'品牌创立时间',
        'shopnum':'门店总数',
        'trademark_all_img':'品牌所有图片',
        'advantage':'加盟优势',
        'slideshow':'产品log图',
        'process':'加盟流程',
        'analysis':'加盟费分析',
        'conditions':'加盟条件',
        'telephone':'固定电话',
        'mobilephone':'移动手机',
        'email':'邮箱地址',
        'fax':'公司传真',
        'corporation':'公司法人',
        'unite':'统一社会信用代码',
        'websiteurl':'品牌官网网址',
        'grade':'品牌评分',
        'trademark_img':'品牌图片',
        'trademark_cp':'品牌产品',
        'trademark_address':'公司地址',
        'trademark_throng':'适合人群',
        'mongo_id':'mongo_id',
        'feeid':'加盟价钱',
        'pattern':'经营模式',
        'title_picture':'品牌商标图片',
        'jiamengnum':'加盟人数',
        'insert_time':'数据插入时间',
        'thumb':'轮播图',
        
        'url':'网站url',
    }

    # ---------------------请求接口参数
    zhaoshang_dict_word02 = {
        'time': 'string请求时间戳',
        'title': 'string招商标题',
        'feeid': 'string加盟费用',
        'thumb': 'string 	缩略图远程地址',
        'keyword': 'string 	关键字',
        'description': 'string 	招商描述',
        'slideshow': 'array 	轮播图片远程地址',
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

    #----------动态赋值2   实现成功
    for k,v in zhaoshang_dict_word02.items():
        locals()[k] = scrapy.Field()

    @property
    def print_value(self):
        for k1, v1 in self.zhaoshang_dict_word.items():
            print('zhaoshang_dicts["{}"] = response.xpath(" ") #{}'.format(k1, v1))
        return 
    
    

#-------------------------品牌字段  item
class MaiGooItem(scrapy.Item):
    # define the fields for your item here like:

    #self word
    url      = scrapy.Field()
    response = scrapy.Field()
    mongo_id = scrapy.Field()
    

    #need word
    fid	            = scrapy.Field()          #行业分类ID
    fid_name	            = scrapy.Field()          #行业分类ID
    title	        = scrapy.Field()          #标题
    thumb	        = scrapy.Field()           #缩略图
    region	        = scrapy.Field()           #省份
    region_name	   = scrapy.Field()           #省份
    address	        = scrapy.Field()          #品牌发源地
    foundtime	    = scrapy.Field()          #品牌创立时间
    corporation     = scrapy.Field()          #公司法人
    telphone	    = scrapy.Field()          #固话
    companyname	    = scrapy.Field()          #公司名称
    websiteurl      = scrapy.Field()          #官网
    content	        = scrapy.Field()          #内容
    slideshow	    = scrapy.Field()          #轮播图
    bid             = scrapy.Field()          #品牌等级（500强。。。）
    grade           = scrapy.Field()          #品牌评分（1-5随机）
    scope           = scrapy.Field()          #经营范围（fid未修改前)
    idenid          = scrapy.Field()          #认证标签(idenid值全部为1)
    email           = scrapy.Field()                                    # #邮箱
    index_item      = scrapy.Field()                                    #排名
    classify_name   = scrapy.Field()                                    #分类名称

    #anader word

    corporation_link    = scrapy.Field()
    websiteurl_info     = scrapy.Field()
    user_comment        = scrapy.Field()
    bid_name            = scrapy.Field()
    update_biaoshi      = scrapy.Field()
    company_address      = scrapy.Field()
    spider_url          = scrapy.Field()        #当前爬取的站点  区分


def alter_price(value):
    '''替换价钱'''

    price_dict = {'0-1': '1',
                 '1-5': '2',
                 '5-10': '3',
                 '10-20': '4',
                 '20-30': '5',
                 '30-50': '5',
                 '50-100': '6',
                 '100-200': '7',
                 '200-300': '7',
                 '300-500': '7',
                 '500-600':'7', }

    value = ''.join(value) if isinstance(value,list) else value
    value = value.split('-') if isinstance(value,str) and '-' in value else value
    if isinstance(value, list):
        value = value[0] if '' not in value  else 5
        value = [l for l in list(price_dict) if int(l.split('-')[1]) >int(value)][0]

    key = price_dict.get(value,'None')
    return key


#-----------------------todo 解决省份分类的问题

def get_region_name_id(key):
    '''获取省份对应id'''
    key = '国际' if key is None else key
    province = {
        '北京':'4052',
        '上海':'4053',
        '天津':'4054',
        '重庆':'4055',
        '河北':'4056',
        '山西':'4057',
        '内蒙古':'4058',
        '辽宁':'4059',
        '吉林':'4060',
        '黑龙江':'4061',
        '江苏':'4062',
        '浙江':'4063',
        '安徽':'4064',
        '福建':'4065',
        '江西':'4066',
        '山东':'4067',
        '河南':'4068',
        '湖北':'4069',
        '湖南':'4070',
        '广东':'4071',
        '广西':'4072',
        '海南':'4073',
        '四川':'4074',
        '贵州':'4075',
        '云南':'4076',
        '西藏':'4077',
        '陕西':'4078',
        '甘肃':'4079',
        '青海':'4080',
        '宁夏':'4081',
        '新疆':'4082',
        '台湾':'4083',
        '香港':'4084',
        '澳门':'4085',
        '国际':'4958',
                }
    if isinstance(key,list):
        key = key[0] if key else ''
    #输入字符中开头字符与 dict 中的key 匹配
    try:
        find_key = ''.join([keys  for keys  in province.keys() if keys is not None and key.startswith(keys)])

        region_data = {'get_region_name':find_key,
                         'get_region_id':province.get(find_key, '4958'),
                         }
        return region_data
    except AttributeError as e:
        print(e)


#-----------






#----------------------------todo 解决行业分类问题

def _get_key_value(table_name):
    '''取出对照表中的键值对'''
    if not setting["MYSQL_HOST"]:
        return None
    conn = pymysql.connect(host=setting["MYSQL_HOST"], db=setting['MYSQL_DBNAME'],
                           user=setting['MYSQL_USER'], password=setting['MYSQL_PASSWORD']
                           , charset='utf8', )
    cursor = conn.cursor()
    sql = "select key_value_json from {} order by id desc limit 1;".format(table_name)
    cursor.execute(sql)
    df = cursor.fetchone()[0]
    result = eval(df)
    return result


table_name = 'key_value_table'
load_json = _get_key_value(table_name)

def get_trademard_fid_id_fid_name(trademark_list):
    '''
    获取可以匹配到的fid_id,和匹配到的fid_name
    :param trademark_list: ['餐饮','餐饮行业']
    :return: {'fid_id':fid,'fid_name':fid_name}
    '''
    # table_name = 'key_value_table'
    # load_json = _get_key_value(table_name)
    fid_data = _trademark_id(trademark_list,load_json)
    return fid_data



def _trademark_id(trademark_list, load_json):
    '''查找品牌对应序列id'''

    # ----------------------------------------
    pp_dict = {'餐饮': '餐饮行业',
               '酒店': '酒店  ',
               '教育': '教育培训',
               '金融': '金融信息',
               '茶叶': '茶叶  ',
               '休闲': '休闲娱乐',
               '家居': '家居生活',
               '家纺': '家纺  ',
               '服装': '服装  ',
               '酒水': '酒饮冲调',
               '汽车': '汽车用品',
               '建材': '装修建材',
               '珠宝': '珠宝首饰',
               '美容': '化妆美容',
               '母婴': '母婴用品',
               '幼教': '幼教  ',
               '宠物': '宠物  ',
               '干洗': '干洗服务',
               '医药': '医疗保健',
               '零售': '商场超市',
               '健身': '生活服务',
               '超市': '商场超市',
               '环保': '低碳环保',
               '其他': '其他  '}

    # --------------------------------------------
    # trademark_list = '餐饮,烘焙店'.split(',')
    # trademark_list = '游戏,烘焙店'.split(',')
    # trademark_list = '建材,防水'.split(',')
    # trademark_list = '孕婴童,母婴护理'.split(',')
    # trademark_list = '医药,医疗用品'.split(',')
    # trademark_list = '环保,专利创新'.split(',')
    # trademark_list = '美容,美瞳'.split(',')
    # trademark_list = '美容,干洗服务'.split(',')
    if len(trademark_list)<2:
        trademark_list=trademark_list*2

    # setp 1 将dict.keys循环，将需查找str 在list 中进行判断，如果str的开始与list 中的str开头可以匹配，将字典中的 key value 取出来
    setp1 = [f for f in load_json.keys() if f.startswith(trademark_list[0]) or f.endswith(trademark_list[0])]
    setp1_0 = [f for f in load_json.keys() if f.startswith(trademark_list[1]) or f.endswith(trademark_list[1])]
    # setp 1.1   优先匹配最深类，自右往左匹配
    setp1_1 = setp1_0 if setp1_0 else setp1
    # print('setp 1',setp1_1)

    # setp 2 如果字符串开始和结尾有匹配到相关数据，取值， 如果没有匹配到，按照硬匹配来匹配
    setp2 = setp1 if setp1 else pp_dict.get(trademark_list[0])
    # print('setp 2',setp2)

    # setp 3 模糊匹配  与硬匹配  比较 ，取存在的值,优先取模糊匹配，再取硬匹配,如果都没有，以自己的第一个字符进行匹配  setp 4
    setp3 = setp1_1 if setp1_1 else setp2
    # print('setp 3',setp3)

    # setp 4 硬匹配，模糊匹配 都无法匹配，进行单一字符匹配,深度优先匹配
    setp4 = [f for f in load_json.keys() if f.startswith(trademark_list[0][0]) or f.endswith(trademark_list[0][0])]
    setp4_0 = [f for f in load_json.keys() if
               f.startswith(trademark_list[1][0]) or f.endswith(trademark_list[1][0])]
    # setp 4.1   模糊>硬匹配>深度匹配
    setp4_1 = setp3 if setp3 else setp4_0 if setp4_0 else setp4
    # print('setp 4',setp4_1)

    # setp 5  模糊匹配，硬匹配，单一匹配   取值
    setp5 = setp3 if setp3 else setp4_1
    # print('setp5',setp5)

    # setp6  将模糊匹配中对应的id取出来
    setp6 = load_json.get(setp5[0])if setp5 else ''
    # print('setp6',setp6)

    # setp7 return 列表转换成str,对应的取值id
    setp7_0 = ','.join(setp5)
    setp7_1 = setp6

    print('setp 7,', start,'fid_name:',setp7_0,' fid_id:', setp7_1)

    # -------------------------------------------
    data = {'fid_id':setp7_1,'fid_name':setp7_0}
    return data







class GetMysql():

    def __init__(self):
        self.docker_mysql_conn = pymysql.Connect(host=setting["MYSQL_HOST"], db=setting['MYSQL_DBNAME'],
                               user=setting['MYSQL_USER'], password=setting['MYSQL_PASSWORD']
                               ,charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.docker_mysql_cursor = self.docker_mysql_conn.cursor()

    def close_mysql(self):
        self.docker_mysql_conn.close()
        self.docker_mysql_cursor.close()
        print('mysql close.')

    def is_json(self,data):
        '''判断是否是json'''
        try:
            json.loads(data)
            return True
        except ValueError as e:
            return False


    def get_one(self,word,value):
        get_one_value = [one for one in self.get_mysql(word,value)]
        return get_one_value

    def get_mysql(self,word,value,number=1):
        '''装饰器输出信息'''
        sql = """select {} from pp_spider where  title='{}'  order by id desc limit {};""".format(word,value,number)
        # sql = """select {} from ye_zhaoshang_data where  update_biaoshi=2 and id=55960  order by id desc  limit {};""".format(word,number)
        self.docker_mysql_cursor.execute(sql)
        df = self.docker_mysql_cursor.fetchall()
        yield from df

    def update_value(self,update_word, update_value, id):
        # 拿到对应的字段名，oss_url,数据库行id
        json_update_value = update_value.replace("'",'"') if update_value else update_value
        update_sql = '''update ye_zhaoshang_data set {}='{}',update_biaoshi=2 where id={} limit 1;'''.format(update_word,json_update_value,id)
        self.docker_mysql_cursor.execute(update_sql)
        self.docker_mysql_conn.commit()
        print('mysql update ok.',id)


    def update_id(self,index_item,title):
        '''如果存在图片无法转换更新update =3'''
        sql = '''update pp_spider set index_item={} where title="{}";'''.format(index_item,title)
        self.docker_mysql_cursor.execute(sql)
        self.docker_mysql_conn.commit()
        print('update id ={}:'.format(index_item),title)
        return True


class GetMysqlV3():

    def __init__(self):
        exists_ = setting['MYSQL_SETTING']["MYSQL_HOST"]
        if exists_:
            self.conn = pymysql.Connect(host=exists_["MYSQL_HOST"], db=exists_['MYSQL_DBNAME'],
                                   user=exists_['MYSQL_USER'], password=exists_['MYSQL_PASSWORD']
                                   , charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.conn.cursor()

    #查
    def get_mysql_one(self,sql):
        self.cursor.execute(sql)
        df = self.cursor.fetchone()
        return df

    def get_mysql_all(self, sql):
        self.cursor.execute(sql)
        df = self.cursor.fetchall()
        return df
        

    def close_mysql(self):
        self.conn.close()
        self.cursor.close()
        print('mysql close.')


    def is_json(self,data):
        '''判断是否是json'''
        try:
            json.loads(data)
            return True
        except ValueError as e:
            return False

    def get_mysql(self,word,value,classify_name):
        '''装饰器输出信息'''
        sql = """select {} from pp_spider_index where  title='{}' and classify_name='{}'  order by id desc limit 1;""".format(word,value,classify_name)
        # sql = """select {} from ye_zhaoshang_data where  update_biaoshi=2 and id=55960  order by id desc  limit {};""".format(word,number)
        print(sql)
        self.cursor.execute(sql)
        df = self.cursor.fetchall()
        yield from df


    def update_value(self,update_word, update_value, id):
        # 拿到对应的字段名，oss_url,数据库行id

        json_update_value = update_value.replace("'",'"') if update_value else update_value
        update_sql = '''update ye_zhaoshang_data set {}='{}',update_biaoshi=2 where id={} limit 1;'''.format(update_word,json_update_value,id)
        # print(update_sql)

        # raise ImportError

        self.cursor.execute(update_sql)
        self.conn.commit()
        print('mysql update ok.',id)

    def update_id(self,classify_name,title):
        '''如果存在图片无法转换更新update =3'''
        sql = '''update pp_spider_index set classify_name="{}" where title="{}" and classify_name="None" limit 1;'''.format(classify_name,title)
        self.cursor.execute(sql)
        self.conn.commit()
        print('update id ={}:'.format(classify_name),title)
        return True





class AlterClassify():

    def __init__(self):
        self.mysql_conn = pymysql.Connect(host=setting["MYSQL_HOST"], db=setting['MYSQL_DBNAME'],
                                                 user=setting['MYSQL_USER'], password=setting['MYSQL_PASSWORD']
                                                 , charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.mysql_cursor = self.mysql_conn.cursor()

    # ----------------------------todo 解决行业分类问题

    def _get_key_value(self,table_name):
        '''取出对照表中的键值对'''

        sql = "select key_value_json from {} order by id desc limit 1;".format(table_name)
        self.mysql_cursor.execute(sql)
        df = self.mysql_cursor.fetchone().get('key_value_json',{})
        dict_df = eval(df)
        return dict_df

    # table_name = 'key_value_table'
    # load_json = _get_key_value(table_name)

    def get_trademard_fid_id_fid_name(self,trademark_list):
        '''
        获取可以匹配到的fid_id,和匹配到的fid_name
        :param trademark_list: ['餐饮','餐饮行业']
        :return: {'fid_id':fid,'fid_name':fid_name}
        '''
        table_name = 'key_value_table'
        load_json = self._get_key_value(table_name)
        # print(load_json)
        fid_data = self._trademark_id(trademark_list,load_json)
        return fid_data


    def _trademark_id(self,trademark_list, load_json):
        '''查找品牌对应序列id'''

        trademark_list = trademark_list * 2 if len(trademark_list) < 2 else trademark_list
        trademark_list = trademark_list[0].split('/') if '/' in trademark_list[0] else trademark_list
        # ----------------------------------------
        pp_dict = {'餐饮': '餐饮行业',
                   '酒店': '酒店  ',
                   '教育': '教育培训',
                   '金融': '金融信息',
                   '茶叶': '茶叶  ',
                   '休闲': '休闲娱乐',
                   '家居': '家居生活',
                   '家纺': '家纺  ',
                   '服装': '服装  ',
                   '酒水': '酒饮冲调',
                   '汽车': '汽车用品',
                   '建材': '装修建材',
                   '珠宝': '珠宝首饰',
                   '美容': '化妆美容',
                   '母婴': '母婴用品',
                   '幼教': '幼教  ',
                   '宠物': '宠物  ',
                   '干洗': '干洗服务',
                   '医药': '医疗保健',
                   '零售': '商场超市',
                   '健身': '生活服务',
                   '超市': '商场超市',
                   '环保': '低碳环保',
                   '其他': '其他  '}

        # --------------------------------------------
        # trademark_list = '餐饮,烘焙店'.split(',')
        # trademark_list = '游戏,烘焙店'.split(',')
        # trademark_list = '建材,防水'.split(',')
        # trademark_list = '孕婴童,母婴护理'.split(',')
        # trademark_list = '医药,医疗用品'.split(',')
        # trademark_list = '环保,专利创新'.split(',')
        # trademark_list = '美容,美瞳'.split(',')
        # trademark_list = '美容,干洗服务'.split(',')

        # setp 1 将dict.keys循环，将需查找str 在list 中进行判断，如果str的开始与list 中的str开头可以匹配，将字典中的 key value 取出来
        setp1 = [f for f in load_json.keys() if f.startswith(trademark_list[0]) or f.endswith(trademark_list[0])]
        setp1_0 = [f for f in load_json.keys() if f.startswith(trademark_list[1]) or f.endswith(trademark_list[1])]
        # setp 1.1   优先匹配最深类，自右往左匹配
        setp1_1 = setp1_0 if setp1_0 else setp1
        # print('setp 1',setp1_1)

        # setp 2 如果字符串开始和结尾有匹配到相关数据，取值， 如果没有匹配到，按照硬匹配来匹配
        setp2 = setp1 if setp1 else pp_dict.get(trademark_list[0])
        # print('setp 2',setp2)

        # setp 3 模糊匹配  与硬匹配  比较 ，取存在的值,优先取模糊匹配，再取硬匹配,如果都没有，以自己的第一个字符进行匹配  setp 4
        setp3 = setp1_1 if setp1_1 else setp2
        # print('setp 3',setp3)

        # setp 4 硬匹配，模糊匹配 都无法匹配，进行单一字符匹配,深度优先匹配
        setp4 = [f for f in load_json.keys() if f.startswith(trademark_list[0][0]) or f.endswith(trademark_list[0][0])]
        setp4_0 = [f for f in load_json.keys() if
                   f.startswith(trademark_list[1][0]) or f.endswith(trademark_list[1][0])]
        # setp 4.1   模糊>硬匹配>深度匹配
        setp4_1 = setp3 if setp3 else setp4_0 if setp4_0 else setp4
        # print('setp 4',setp4_1)

        # setp 5  模糊匹配，硬匹配，单一匹配   取值
        setp5 = setp3 if setp3 else setp4_1
        # print('setp5',setp5)

        # setp6  将模糊匹配中对应的id取出来
        setp6 = load_json.get(setp5[0]) if setp5 else ''
        # print('setp6',setp6)

        # setp7 return 列表转换成str,对应的取值id
        setp7_0 = ','.join(setp5)
        setp7_1 = setp6

        print('setp 7,', start, 'fid_name:', setp7_0, ' fid_id:', setp7_1)

        # -------------------------------------------
        data = {'fid_id': setp7_1, 'fid_name': setp7_0}
        return data


    def _trademark_id_v2(self,trademark_list, load_json):
        '''查找品牌对应序列id'''

        trademark_list = trademark_list * 2 if len(trademark_list) < 2 else trademark_list
        trademark_list = trademark_list[0].split('/') if '/' in trademark_list[0] else trademark_list
        # ----------------------------------------
        pp_dict = {'餐饮': '餐饮行业',
                   '酒店': '酒店  ',
                   '教育': '教育培训',
                   '金融': '金融信息',
                   '茶叶': '茶叶  ',
                   '休闲': '休闲娱乐',
                   '家居': '家居生活',
                   '家纺': '家纺  ',
                   '服装': '服装  ',
                   '酒水': '酒饮冲调',
                   '汽车': '汽车用品',
                   '建材': '装修建材',
                   '珠宝': '珠宝首饰',
                   '美容': '化妆美容',
                   '母婴': '母婴用品',
                   '幼教': '幼教  ',
                   '宠物': '宠物  ',
                   '干洗': '干洗服务',
                   '医药': '医疗保健',
                   '零售': '商场超市',
                   '健身': '生活服务',
                   '超市': '商场超市',
                   '环保': '低碳环保',
                   '其他': '其他  '}


        # setp 1 将dict.keys循环，将需查找str 在list 中进行判断，如果str的开始与list 中的str开头可以匹配，将字典中的 key value 取出来
        setp1 = [f for f in load_json.keys() if f.startswith(trademark_list[0]) or f.endswith(trademark_list[0])]
        setp1_0 = [f for f in load_json.keys() if f.startswith(trademark_list[1]) or f.endswith(trademark_list[1])]
        # setp 1.1   优先匹配最深类，自右往左匹配
        setp1_1 = setp1_0 if setp1_0 else setp1
        # print('setp 1',setp1_1)

        # setp 2 如果字符串开始和结尾有匹配到相关数据，取值， 如果没有匹配到，按照硬匹配来匹配
        setp2 = setp1 if setp1 else pp_dict.get(trademark_list[0])
        # print('setp 2',setp2)

        # setp 3 模糊匹配  与硬匹配  比较 ，取存在的值,优先取模糊匹配，再取硬匹配,如果都没有，以自己的第一个字符进行匹配  setp 4
        setp3 = setp1_1 if setp1_1 else setp2
        # print('setp 3',setp3)

        # setp 4 硬匹配，模糊匹配 都无法匹配，进行单一字符匹配,深度优先匹配
        setp4 = [f for f in load_json.keys() if f.startswith(trademark_list[0][0]) or f.endswith(trademark_list[0][0])]
        setp4_0 = [f for f in load_json.keys() if
                   f.startswith(trademark_list[1][0]) or f.endswith(trademark_list[1][0])]
        # setp 4.1   模糊>硬匹配>深度匹配
        setp4_1 = setp3 if setp3 else setp4_0 if setp4_0 else setp4
        # print('setp 4',setp4_1)

        # setp 5  模糊匹配，硬匹配，单一匹配   取值
        setp5 = setp3 if setp3 else setp4_1
        # print('setp5',setp5)

        # setp6  将模糊匹配中对应的id取出来
        setp6 = load_json.get(setp5[0]) if setp5 else ''
        # print('setp6',setp6)

        # setp7 return 列表转换成str,对应的取值id
        setp7_0 = ','.join(setp5)
        setp7_1 = setp6

        print('setp 7,', start, 'fid_name:', setp7_0, ' fid_id:', setp7_1)

        # -------------------------------------------
        data = {'fid_id': setp7_1, 'fid_name': setp7_0}
        return data

    def get_region_name_id(self,key):
        '''获取省份对应id'''
        key = '国际' if key is None else key
        province = {
            '北京': '4052',
            '上海': '4053',
            '天津': '4054',
            '重庆': '4055',
            '河北': '4056',
            '山西': '4057',
            '内蒙古': '4058',
            '辽宁': '4059',
            '吉林': '4060',
            '黑龙江': '4061',
            '江苏': '4062',
            '浙江': '4063',
            '安徽': '4064',
            '福建': '4065',
            '江西': '4066',
            '山东': '4067',
            '河南': '4068',
            '湖北': '4069',
            '湖南': '4070',
            '广东': '4071',
            '广西': '4072',
            '海南': '4073',
            '四川': '4074',
            '贵州': '4075',
            '云南': '4076',
            '西藏': '4077',
            '陕西': '4078',
            '甘肃': '4079',
            '青海': '4080',
            '宁夏': '4081',
            '新疆': '4082',
            '台湾': '4083',
            '香港': '4084',
            '澳门': '4085',
            '国际': '4958',
        }
        if isinstance(key, list):
            key = key[0] if key else ''
        # 输入字符中开头字符与 dict 中的key 匹配
        try:
            find_key = ''.join([keys for keys in province.keys() if keys is not None and key.startswith(keys)])

            region_data = {'get_region_name': find_key,
                           'get_region_id': province.get(find_key, '4958'),
                           }
            return region_data
        except AttributeError as e:
            print(e)




if __name__ == "__main__":
    # get_mysql = GetMysqlV3()
    # g = get_mysql.get_one('title','韩都衣舍HSTYLE','穿着/装扮')
    # print(g)



    alter_result = alter_price(['10'])
    print(alter_result)
