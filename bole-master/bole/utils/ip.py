import requests
import random
import json
from scrapy.selector import Selector
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

conn = pymysql.connect('localhost', 'root', '****', 'lyh', charset='utf8',use_unicode=True)
cursor = conn.cursor()
class GetIP(object):
    def get_random_ip(self):
        #从数据库中随机获取一个可用的ip
        random_sql = """
              SELECT ip FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            print("http://{0}".format(ip))
            return "http://{0}".format(ip)
# print (crawl_ips())
if __name__ == "__main__":
    get_ip = GetIP()
    get_ip.get_random_ip()