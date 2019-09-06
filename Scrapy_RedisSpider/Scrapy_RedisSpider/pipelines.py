# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
start = '*'*20


import pymongo
from Scrapy_RedisSpider.items import MaiGooItem,ZhaoShanItem,CompanyItems
class MongoPipeline(object):

    #mongo文件名
    collection_name = 'qianjin_data_v2'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri      = mongo_uri
        self.mongo_db       = mongo_db
        self.mongo_table    = 'pp_data'


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def process_item2(self, item, spider):
        res = self.db[self.mongo_table].insert_one(dict(item if item else {}))
        mongo_id = str(res.inserted_id)
        # 将response替换成Mongo id,添加到item中，后面插入mysql
        item._values['mongo_id'] = mongo_id
        item._values['contents'] = mongo_id
        item._values['content'] = mongo_id
        item._values['advantage'] = mongo_id
        item._values['process'] = mongo_id
        print(start,'insert mongo id {} ok.'.format(mongo_id))
        return item


    def process_item(self, item, spider):

        """ 判断item的类型，并作相应的处理，再入数据库 """

        #--------------品牌数据
        mongo_id = None
        if isinstance(item, MaiGooItem):
            try:
                res = self.db[self.mongo_table].insert_one(dict(item))
                mongo_id = str(res.inserted_id)
                item._values['mongo_id'] = mongo_id
                item._values['contents'] = mongo_id
                item._values['content'] = mongo_id
                item._values['advantage'] = mongo_id
                item._values['process'] = mongo_id
            except Exception as e:
                print(e)
        #------------------招商数据
        elif isinstance(item, ZhaoShanItem):
            try:
                res = self.db[self.mongo_table].insert_one(dict(item))
                mongo_id = str(res.inserted_id)
                item._values['mongo_id'] = mongo_id
                item._values['contents'] = mongo_id

            except Exception as e:
                print(e)
        #----------------企业数据
        elif isinstance(item, CompanyItems):
            try:
                res = self.db[self.mongo_table].insert_one(dict(item))
                mongo_id = str(res.inserted_id)
                item._values['mongo_id'] = mongo_id
            except Exception as e :
                print(e)
            #---------没有公司名字的不处理
            if item._values['company_name'] is None:
                return
        print(start, 'insert mongo id {} ok.'.format(mongo_id))
        return item


    def close_spider(self, spider):
        self.client.close()





# -----------------------------------todo pipeline 异步插入mysql
from pymysql import IntegrityError

import pymysql
from twisted.enterprise import adbapi
class MysqlTwistedPipeline(object):

    def __init__(self, dbpool):
        self.table_name = None
        self.dbpools = dbpool
        self.zhaoshang_table = 'ye_zhaoshang_data'
        self.pingpai_table = 'ye_zhaoshang_data'
        self.company_table = 'pp_company_info'
        self.dbpool = adbapi.ConnectionPool("pymysql", **self.dbpools)

    @classmethod
    def from_settings(cls, settings):
        '''从配置中获取信息'''
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        return cls(dbparms)


    def process_item2(self, item, spider):
        '''异步插入mysql'''
        # query = self.dbpool.runInteraction(self.do_insert, item)
        query = self.dbpool.runInteraction(self.insert_databases, item)
        # query.addErrorback(self.handle_error)
        query.addErrback(self.handle_error)
        print(start, 'insert mysql ok ',item['title'])


    def process_item(self, item, spider):
        # ----------多张表插入
        if isinstance(item, MaiGooItem):
            self.table_name = self.pingpai_table
        elif isinstance(item, ZhaoShanItem):
            self.table_name = self.zhaoshang_table
        elif isinstance(item, CompanyItems):
            self.table_name = self.company_table
        else:
            print('insert table is None')
            return

        query = self.dbpool.runInteraction(self.insert_databases, item)
        # query.addErrorback(self.handle_error)
        query.addErrback(self.handle_error)
        print(start, 'insert mysql ok {}'.format(self.table_name))


    def handle_error(self, falure):
        '''错误处理'''
        print(start, 'handle_error', falure)
        

    def do_insert(self, cursor, item):
        '''执行插入语句'''
        insert_sql = """
                    insert into qianjin_data(response_txt,url)
                    VALUES (%s,%s);
                    """
        cursor.execute(insert_sql, (item['response_txt'], item['url']))


    def insert_databases(self, cursor, item):
        # -------------插入数据库-------------------
        # --------------添加数据库的唯一约束
        '''
            alter table f_call_loan add unique index(order_number,biaoshi);

            alter table f_model_word add unique index(order_number,idcard);
        '''
        error_list = []
        try:
            if isinstance(item, list):
                for table_dict in item:
                    # ------------------插入测试库
                    a = ','.join('{}'.format(key) for key in table_dict.keys())
                    b = ','.join("'{}'".format(value) for value in table_dict.values())
                    insert_dict = "INSERT INTO {} ({})VALUES({})".format(self.table_name, a, b);
    
                    cursor.execute(insert_dict)
                print('commit ok for {}'.format(self.table_name))
            # elif isinstance(table_source,dict):
            else:
                a = ','.join('{}'.format(key) for key in item.keys())
                # b = ','.join('"{}"'.format(value.replace('\\','').replace('"', "'") if isinstance(value,str) else value)
                #              for value in item.values())

                b = ','.join('"{}"'.format(
                    value.replace('\\', '').replace('"', ' ').replace("'", '') if isinstance(value, str) else value)
                             for value in item.values())

                insert_dict = "INSERT INTO {} ({})VALUES({})".format(self.table_name, a, b);
                cursor.execute(insert_dict)
                print('commit ok for {}'.format(self.table_name))

                # -----本地库提交
        except IntegrityError as e:
            print("Error: {}".format(e))
            error_list.append('{}'.format(e))
            raise IntegrityError
        # except Exception as e:
        #     print("Error: {}".format(e))
        insert_status = {
            'code': '{}'.format(200 if len(error_list) < 1 else 300),
            'insert_status': '{}'.format(''.join(error_list if error_list else 'ok')),
        }
        print('insert database ok')
        return insert_status

    def close_spider(self, spider):
        pass



class PpRedisspiderPipeline(object):
    def process_item(self, item, spider):
        return item
