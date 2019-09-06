# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import json

import pymysql
import scrapy
from scrapy.utils.project import get_project_settings
setting = get_project_settings()
start = '*'*15


#-------------------------maigoo  item
class MaiGooItem(scrapy.Item):
    # define the fields for your item here like:

    url      = scrapy.Field()
    response = scrapy.Field()
    mongo_id = scrapy.Field()
    navigation_name = scrapy.Field()
    navigation_link = scrapy.Field()
    trademark_throng = scrapy.Field()
    trademark_address = scrapy.Field()






#----------------------------qj_item        2019.06.09    yfl
class PpSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    manage          = scrapy.Field()
    companyname     = scrapy.Field()
    source          = scrapy.Field()
    shopnum         = scrapy.Field()
    slideshow       = scrapy.Field()
    content         = scrapy.Field()
    foundtime       = scrapy.Field()
    trademark_address = scrapy.Field()
    process         = scrapy.Field()
    advantage       = scrapy.Field()
    trademark_cp    = scrapy.Field()
    trademark_throng = scrapy.Field()
    fid             = scrapy.Field()
    trademark_all_img = scrapy.Field()
    title           = scrapy.Field()
    feeid           = scrapy.Field()
    pattern         = scrapy.Field()
    mongo_id        = scrapy.Field()
    title_picture   = scrapy.Field()
    region          = scrapy.Field()
    region_name     = scrapy.Field()
    thumb           = scrapy.Field()
    fid_name        = scrapy.Field()  



    def get_region_name_id(self,key):
        '''获取省份对应id'''
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

        region_data = {'get_region_name':key,
                         'get_region_id':province.get(key, 'None'),
                         }
        return region_data





    def alter_price(self,value):
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
                     '500':'7', }
        key = price_dict.get(value,'None')
        return key


    def get_key_value(self):
        '''取出对照表中的键值对'''
        table_name = 'key_value_table'
        conn = pymysql.connect(host=setting["MYSQL_HOST"], db=setting['MYSQL_DBNAME'],
                               user=setting['MYSQL_USER'], password=setting['MYSQL_PASSWORD']
                               , charset='utf8', )
        cursor = conn.cursor()
        sql = "select key_value_json from {} order by id desc limit 1;".format(table_name)
        cursor.execute(sql)
        df = cursor.fetchone()[0]
        return eval(df)



    def get_trademard_fid_id_fid_name(self,trademark_list):
        '''
        获取可以匹配到的fid_id,和匹配到的fid_name
        :param trademark_list: ['餐饮','餐饮行业']
        :return: {'fid_id':fid,'fid_name':fid_name}
        '''
        load_json = self.get_key_value()
        fid_data = self.trademark_id(trademark_list,load_json)
        return fid_data


    def trademark_id(self,trademark_list, load_json):
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
        setp6 = load_json.get(setp5[0])
        # print('setp6',setp6)

        # setp7 return 列表转换成str,对应的取值id
        setp7_0 = ','.join(setp5)
        setp7_1 = setp6

        print('setp 7,', start,'fid_name:',setp7_0,' fid_id:', setp7_1)

        # -------------------------------------------
        data = {'fid_id':setp7_1,'fid_name':setp7_0}
        return data











# trademark_list = '餐饮,烘焙店'.split(',')

def trademark_id(trademark_list,load_json):
    '''查找品牌对应序列id'''
    # if isinstance(trademark_list, list):
    #     with open(r'../static/key_value.json', 'r') as f:
    #         json_data = f.read()
    #         load_json = json.loads(json_data)
    #
    #         print(load_json.keys())

            # value = load_json.get(trademark[0]) if load_json.get(trademark[0]) else load_json.get(trademark[1])

            #----------------------------------------
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

    #--------------------------------------------
    # trademark_list = '餐饮,烘焙店'.split(',')
    # trademark_list = '游戏,烘焙店'.split(',')
    # trademark_list = '建材,防水'.split(',')
    # trademark_list = '孕婴童,母婴护理'.split(',')
    # trademark_list = '医药,医疗用品'.split(',')
    # trademark_list = '环保,专利创新'.split(',')
    # trademark_list = '美容,美瞳'.split(',')
    #trademark_list = '美容,干洗服务'.split(',')


    #setp 1 将dict.keys循环，将需查找str 在list 中进行判断，如果str的开始与list 中的str开头可以匹配，将字典中的 key value 取出来
    setp1  = [f for f in load_json.keys() if f.startswith(trademark_list[0]) or f.endswith(trademark_list[0])]
    setp1_0  = [f for f in load_json.keys() if f.startswith(trademark_list[1]) or f.endswith(trademark_list[1])]
    # setp 1.1   优先匹配最深类，自右往左匹配
    setp1_1 = setp1_0 if setp1_0 else setp1
    # print('setp 1',setp1_1)

    #setp 2 如果字符串开始和结尾有匹配到相关数据，取值， 如果没有匹配到，按照硬匹配来匹配
    setp2  = setp1 if setp1 else pp_dict.get(trademark_list[0])
    # print('setp 2',setp2)

    #setp 3 模糊匹配  与硬匹配  比较 ，取存在的值,优先取模糊匹配，再取硬匹配,如果都没有，以自己的第一个字符进行匹配  setp 4
    setp3 = setp1_1 if setp1_1 else setp2
    # print('setp 3',setp3)

    #setp 4 硬匹配，模糊匹配 都无法匹配，进行单一字符匹配,深度优先匹配
    setp4 = [f for f in load_json.keys() if f.startswith(trademark_list[0][0]) or f.endswith(trademark_list[0][0])]
    setp4_0 = [f for f in load_json.keys() if f.startswith(trademark_list[1][0]) or f.endswith(trademark_list[1][0])]
    # setp 4.1   模糊>硬匹配>深度匹配
    setp4_1 = setp3 if setp3 else setp4_0 if setp4_0 else setp4
    # print('setp 4',setp4_1)

    #setp 5  模糊匹配，硬匹配，单一匹配   取值
    setp5 = setp3 if setp3 else setp4_1
    # print('setp5',setp5)

    #setp6  将模糊匹配中对应的id取出来
    setp6 = load_json.get(setp5[0])
    # print('setp6',setp6)


    #setp7 return 列表转换成str,对应的取值id
    setp7_0 = ','.join(setp5)
    setp7_1 = setp6

    print('setp 7,',setp7_0,setp7_1)

    #-------------------------------------------
    return setp7_0,setp7_1



# print(trademark_list)
# t = trademark_id(trademark_list)
# print(t)


# with open(r'../static/key_value.json', 'r') as f:
#     json_data = f.read()
#     load_json = json.loads(json_data)
#     print(load_json)
#















