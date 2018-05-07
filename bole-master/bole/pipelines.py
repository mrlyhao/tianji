# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import pymysql,redis
import pymysql.cursors
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import asyncio

class LagouMysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):#调用settings值的固定函数，调用方法和字典一样
        # 将参数字典化方便传入
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset= 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,

        )
        # from twisted.enterprise import adbapi  Twisted为数据库提供的一个异步化接口。
        dbpool = adbapi.ConnectionPool('pymysql',**dbparms)#第一个是需要的函数名称，后边是不定长的字典参数

        return  cls(dbpool)
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)#处理异常

    def handle_error(self,failure):
        #处理异步插入异常
        print(failure)
    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql,params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

class BolePipeline(object):
    def process_item(self, item, spider):
        return item#返回item值，因为其余的管道还要使用item
class MysqlPipeline(object):
    # 采用同步的机制写入MySQL
    def __init__(self):
        #链接数据库
        self.conn = pymysql.connect('localhost','root','****','lyh',charset='utf8',use_unicode = True)#mysql使用的是gbk，而python使用的是ut8，所以鼻血设定后两个参数，后一个参数为是否使用字符集
        #创建数据库浮标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 设置需要插入的行的名称
        insert_sql = """
            insert into jobbole_acticle(title,url,create_date,fav_nums)       
             VALUES (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item['title'],item['url'],item['create_date'],item['fav_nums']))
        # 完成插入后提交
        self.conn.commit()

class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):#调用settings值的固定函数，调用方法和字典一样
        # 将参数字典化方便传入
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset= 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,

        )
        # from twisted.enterprise import adbapi  Twisted为数据库提供的一个异步化接口。
        dbpool = adbapi.ConnectionPool('pymysql',**dbparms)#第一个是需要的函数名称，后边是不定长的字典参数

        return  cls(dbpool)
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)#处理异常

    def handle_error(self,failure):
        #处理异步插入异常
        print(failure)
    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
            insert into jobbole_acticle(title,url,url_object_id,create_date,front_image_url,praise_nums,fav_nums,tags,content,comment_nums)       
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql, (item['title'], item['url'],item['url_object_id'],item['create_date'], item['front_image_url'],
                                    item['praise_nums'],item['fav_nums'],item['tags'],item['content'],item['comment_nums']))

class QiyeTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):#调用settings值的固定函数，调用方法和字典一样
        # 将参数字典化方便传入
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset= 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,

        )
        # from twisted.enterprise import adbapi  Twisted为数据库提供的一个异步化接口。
        dbpool = adbapi.ConnectionPool('pymysql',**dbparms)#第一个是需要的函数名称，后边是不定长的字典参数

        return  cls(dbpool)
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)#处理异常

    def handle_error(self,failure):
        #处理异步插入异常
        print(failure)
    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into qichacha_zuixin(url,conpany_id,company,tel,email,www,addr,delegate,login_money,real_money,status,login_time,Registration,org_number,
                          taxpayer_number,credit_number,company_type,profession,approved_date,registration_org,region,english_name,
                          old_name,business_mode,staff_size,business_date,business_scope,partner_info,main_member,touzilist,fenzhilist,changelist)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql,(item['url'],item['conpany_id'],item['company'],item['tel'],item['email'],item['www'],item['addr'],
                                                 item['delegate'],item['login_money'],item['real_money'],item['status'],item['login_time'],item['Registration'],item['org_number'],
                                                 item['taxpayer_number'],item['credit_number'],item['company_type'],item['profession'],item['approved_date'],item['registration_org'],
                                                 item['region'],item['english_name'],item['old_name'],item['business_mode'],item['staff_size'],item['business_date'],item['business_scope'],
                                                item['partner_info'],item['main_member'],item['touzilist'],item['fenzhilist'],item['changelist']))


class RdisPipline(object):
    def __init__(self):
        #链接数据库
        self.r = redis.Redis(host='39.104.62.136', port=6379,db=0)
    def process_item(self, item, spider):
        loop = asyncio.get_event_loop()
        # 设置需要插入的行的名称
        import json
        @asyncio.coroutine
        def go():
            jieguo = json.dumps(dict(item))
            self.r.lpush('json', jieguo)
            self.r.lpush('shuliang', jieguo)
        loop.run_until_complete(go())
        print('成功倒入redis=============================================================================================')