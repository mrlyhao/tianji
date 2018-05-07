import requests
import random
import json
from scrapy.selector import Selector
import pymysql
import pymysql.cursors
import time

conn = pymysql.connect('localhost', 'root', '****', 'lyh', charset='utf8',use_unicode=True)
cursor = conn.cursor()
set=set()
def get_ip():
    try:
        url='http://dly.134t.com/query.txt?key=NP100B7199&word=&count=10'
        web_data=requests.get(url).text.split('\n')
        for data in web_data:
            data=data.strip()
            if data not in set:
                set.add(data)
                print(data)
                cursor.execute(
                    "insert into proxy_ip(ip) VALUES('{0}')".format(data)
                )
                conn.commit()
    except:
        return ''

random_sql = """
              SELECT ip FROM proxy_ip
            ORDER BY RAND()
            """
cursor.execute(random_sql)
ip_infos = cursor.fetchall()
shuliang=len(ip_infos)
print(shuliang)
while 1:
    while shuliang<100:
        get_ip()
        random_sql = """
                      SELECT ip FROM proxy_ip
                    ORDER BY RAND()
                    """
        cursor.execute(random_sql)
        ip_infos = cursor.fetchall()
        shuliang = len(ip_infos)
        print(shuliang)
        time.sleep(1)