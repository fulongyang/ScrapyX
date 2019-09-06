# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql import IntegrityError
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
import pymongo
import redis


setting = get_project_settings()
start = '*'*30



class PpSpiderPipeline(object):
    def process_item(self, item, spider):
        return item



# --------------异步插入mysql
class MysqlTwistedPipeline(object):

    def __init__(self, dbpool, table_name):
        self.dbpool = dbpool
        self.table_name = table_name


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
        table_name = settings['MYSQL_TABLE']
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool, table_name)

    def process_item(self, item, spider):
        '''异步插入mysql'''
        # query = self.dbpool.runInteraction(self.do_insert, item)
        query = self.dbpool.runInteraction(self.insert_databases, item)
        # query.addErrorback(self.handle_error)
        query.addErrback(self.handle_error)
        print(start, 'insert mysql ok ')

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

    # def insert_databases(self,conn,cursor,table_name, table_source):
    def insert_databases(self, cursor, item):
        table_name = self.table_name

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
                    insert_dict = "INSERT INTO {} ({})VALUES({})".format(table_name, a, b);

                    cursor.execute(insert_dict)

                print('commit ok for {}'.format(table_name))
            # elif isinstance(table_source,dict):
            else:
                a = ','.join('{}'.format(key) for key in item.keys())
                b = ','.join('"{}"'.format(value.replace('\\','').replace('"', ' ').replace("'", '') if isinstance(value,str) else value)
                             for value in item.values())
                insert_dict = "INSERT INTO {} ({})VALUES({})".format(table_name, a, b);
                cursor.execute(insert_dict)
                print('commit ok for {}'.format(table_name))

                # -----本地库提交
        except IntegrityError as e:
            print("Error: {}".format(e))
            error_list.append('{}'.format(e))
        # except Exception as e:
        #     print("Error: {}".format(e))
        insert_status = {
            'code': '{}'.format(200 if len(error_list) < 1 else 300),
            'insert_status': '{}'.format(''.join(error_list if error_list else 'ok')),
        }
        print('insert database ok.')
        return insert_status






#-----------------保存到mongo
class MongoPipeline(object):

    #mongo文件名
    collection_name = 'qianjin_data_v2'

    def __init__(self, mongo_uri, mongo_db,mongo_table):
        self.mongo_uri      = mongo_uri
        self.mongo_db       = mongo_db
        self.mongo_table    = mongo_table


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_table = crawler.settings.get('MONGO_TABLE'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        res = self.db[self.mongo_table].insert_one(dict(item if item else {}))
        mongo_id = str(res.inserted_id)
        # 将response替换成Mongo id,添加到item中，后面插入mysql
        item._values['mongo_id'] = mongo_id
        print(start,'insert mongo id {} ok.'.format(mongo_id))
        return item

    def close_spider(self, spider):
        self.client.close()








