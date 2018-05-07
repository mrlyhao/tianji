# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from fake_useragent import UserAgent
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
from bole.utils.ip import GetIP
from bole.utils.zhandaye import get_ip
import requests
import json
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
from bole.utils.yanzheng import YanzhengIP
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class BoleSpiderMiddleware(object):
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

# class UserAgentMiddleware(object):
#     user_agent_list = [
#         "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
#         "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#         "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
#         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
#         "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
#         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
#         "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
#         "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
#         "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
#         "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
#         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
#         "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
#         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
#         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
#         "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
#         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
#         "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
#         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
#         "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
#         "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
#         "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
#         "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
#         "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#     ]
#     UA = random.choice(user_agent_list)
#
#     def process_request(self,request,spider):
#         UA = random.choice(self.user_agent_list)
#         request.headers['User-Agent'] = UA

class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    def __init__(self,crawler):
        super(RandomUserAgentMiddlware,self).__init__()#super的作用是获取父类的初始方法，这里是获取一个类方法
        self.ua = UserAgent()#这里是引进的一个随机UA的模块
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)#获取crawler，其中包括setting

    def process_request(self,request,spider):
        # print(request.headers)
        def get_ua():
            return getattr(self.ua,self.ua_type)#getattr函数可以根据传递的后边参数的不同，获取前边函数的不同值方法，类似与'.'
        random_ua = get_ua()
        request.headers.setdefault('User_Agent',random_ua)

class RandomProxyMiddleware(object):
    # #使用异步化接口提取IP，否则会造成堵塞。
    # def __init__(self, dbpool):
    #     self.dbpool = dbpool
    #
    # @classmethod
    # def from_settings(cls, settings):  # 调用settings值的固定函数，调用方法和字典一样
    #     # 将参数字典化方便传入
    #     dbparms = dict(
    #         host=settings['MYSQL_HOST'],
    #         db=settings['MYSQL_DBNAME'],
    #         user=settings['MYSQL_USER'],
    #         passwd=settings['MYSQL_PASSWD'],
    #         charset='utf8',
    #         cursorclass=pymysql.cursors.DictCursor,
    #         use_unicode=True,
    #
    #     )
    #     # from twisted.enterprise import adbapi  Twisted为数据库提供的一个异步化接口。
    #     dbpool = adbapi.ConnectionPool('pymysql', **dbparms)  # 第一个是需要的函数名称，后边是不定长的字典参数
    #     return cls(dbpool)
    #
    # def process_request(self, request, spider):
    #     # 使用twisted将mysql读取变成异步执行
    #     query = self.dbpool.runInteraction(self.get_random_ip, request)
    #     query.addErrback(self.handle_error)  # 处理异常
    #
    # def handle_error(self, failure):
    #     # 处理异步插入异常
    #     print(failure)
    #
    # def get_random_ip(self, cursor, request):
    #     # 从数据库中随机获取一个可用的ip
    #     random_sql = """
    #           SELECT ip FROM proxy_ip
    #         ORDER BY RAND()
    #         LIMIT 1
    #         """
    #     result = cursor.execute(random_sql)
    #     for ip_info in cursor.fetchall():
    #         ip = ip_info['ip']
    #         print("http://{0}".format(ip))
    #         request.meta["proxy"] = "http://{0}".format(ip)
    #         # cursor.commit()
    #动态设置ip代理
    def process_request(self, request, spider):
        while True:
            try:
                with open(r'E:\bole-master\bole\utils\proxies.txt', 'r') as f:
                    proxies = f.readlines()
                proxy = random.choice(proxies).strip()
                print(proxy)
                # request.headers.setdefault('Host', 'www.qichacha.com')
                request.meta["proxy"] = proxy
                break
            except:
                time.sleep(1)
                continue
    # def process_exception(self, request, exception, spider):
    #     # 出现异常时（超时）使用代理
    #     while True:
    #         try:
    #             with open(r'E:\bole\bole\utils\proxies.txt', 'r') as f:
    #                 proxies = f.readlines()
    #             proxy = random.choice(proxies).strip()
    #             print(proxy)
    #             # request.headers.setdefault('Host', 'www.qichacha.com')
    #             request.meta["proxy"] = proxy
    #             break
    #         except:
    #             continue
    #     return request

    # def get_random_proxy(self):
    #     '''随机从文件中读取proxy'''
    #     with open(r'E:\bole\bole\utils\proxies.txt', 'r') as f:
    #         proxies = f.readlines()
    #     proxy = random.choice(proxies).strip()
    #     print(proxy)
    #     return proxy

class LocalRetryMiddleware(RetryMiddleware):
    #重试设置，如果代理IP请求异常则重新获取。
    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        # 如果URL中没有firm，则不进行下面的操作。
        if 'firm' in response.url:
            try:
                login_money = response.xpath('//*[@id="Cominfo"]/table[2]//tr[1]/td[2]/text()').extract_first().strip()
            except Exception as e:
                reason=e
                #下方为返回重试
                return self._retry(request, reason, spider) or response
        return response


class JSPageMiddleware(object):


    #通过Chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == "comment":
            broswer = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
            self.broswer.get(request.url)
            time.sleep(3)
            print("访问：{}").format(request.url)

            return HtmlResponse(url=spider.broswer.current_url,body=spider.broswer.page_source,encoding='utf-8',request = request)

# import datetime
# import logging
# import string
# import threading
# import pandas as pd
# import random
#
# from PyMysqlPool import ConnectionPool
#
# logging.basicConfig(format='[%(asctime)s][%(name)s][%(module)s.%(lineno)d][%(levelname)s] %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     level=logging.ERROR)
# config = {
#     'pool_name': 'test',
#     'host': 'localhost',
#     'port': 3306,
#     'user': 'root',
#     'password': '',
#     'database': 'lyh',
#     'pool_resize_boundary': 50,
#     'enable_auto_resize': True,
#     # 'max_pool_size': 10
# }
#
#
# def conn_pool():
#     # pool = MySQLConnectionPool(**config)
#     pool = ConnectionPool(**config)
#     # pool.connect()
#     # print(pool)
#     return pool

