import requests
import random
import json
from scrapy.selector import Selector
import pymysql
import pymysql.cursors
import time

conn = pymysql.connect('localhost', 'root', '****', 'lyh', charset='utf8',use_unicode=True)
cursor = conn.cursor()
def get_ip():
    try:
        url='http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=0ed287c62a7245e6a767274fcb8908c3&count=10&expiryDate=0&format=1'
        web_data=requests.get(url).text
        data = json.loads(web_data)
        print(data)
        data1=data['msg']
    except:
        return ''
    ip_list=[]
    for i in data1:
        ip=i['ip']
        port=i['port']
        final=str(ip)+':'+str(port)
        print(final)
        cursor.execute(
            "insert into proxy_ip(ip) VALUES('{0}')".format(final)
        )
        conn.commit()
if __name__ == "__main__":
    while True:
        try:
            get_ip()
            print('重新验证————————————')
            time.sleep(20)
        except:
            time.sleep(10)
            continue
    # get_ip()