import requests
import random
import time,json
from bole.utils.ip import GetIP
# def get_ip():
#     try:
#         url = 'http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=cbe38c89bc214e088c0a33eeb7280ac9&returnType=2&count=1'
#         web_data=requests.get(url).text
#         data = json.loads(web_data)
#         data1=data['RESULT']
#         print(data1)
#     except:
#         return ''
#     ip_list=[]
#     for i in data1:
#         ip=i['ip']
#         port=i['port']
#         final=str(ip)+':'+str(port)
#         ip="http://{0}".format(final)
#         print(ip)
#         try:
#             tianyancha(ip)
#         except:
#             continue

def tianyancha():
    # url = 'http://www.whatismyip.com.tw/'
    urls=['http://www.qichacha.com/csusong_c70a55cb048c8e4db7bca357a2c113e0.html']
    # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',}
    # a= requests.get(url,headers=headers,proxies=proxies,timeout=5).text
    for url1 in urls:
        # print(url1)
        user_agent_list = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        ]
        UA = random.choice(user_agent_list)
        # print(UA)
        headers1 = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            # 'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            # 'Cookie':'YCID=65c17ff0362511e8af0407cb1a76e068; undefined=65c17ff0362511e8af0407cb1a76e068; ssuid=7651366445; RTYCID=900dc3faa48a4fcf8818f36b47133944; aliyungf_tc=AQAAAECnJSx0dgYAZNrq3R6uWg7xQpEl; csrfToken=3A7aGXkzp1GsDL7rJGIqM4CK; token=8e6dfd47978546d4aff502e43761a4c8; _utm=c255b3af39c54b65ad1354a08af9b95a; jsid=SEM-BAIDU-PP-SY-000257; bannerFlag=true; Hm_lvt_d5ceb643638c8ee5fbf79d207b00f07e=1522651024,1522652784,1522653158; Hm_lpvt_d5ceb643638c8ee5fbf79d207b00f07e=1522654019; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1522655201,1522655212,1522655219,1522656386; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1522656386',
            'Host': 'www.qichacha.com',
            # 'Referer': 'http://www.qichacha.com/',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': UA,
        }
        ge_ip=GetIP()
        ip=ge_ip.get_random_ip()
        print(ip)
        # with open(r'E:\bole\bole\utils\proxies.txt', 'r') as f:
        #     proxies = f.readlines()
        # proxy = random.choice(proxies).strip()
        print(ip)
        proxies_1={'http':ip}
        # print(proxy)
        b= requests.get(url1,headers=headers1,proxies=proxies_1,timeout=5).text
        # with open('baidu.html','w',encoding='utf-8') as f:
        #     # print(web_data)
        #     f.write(web_data)
        if 'document.location.reload' in b:
            print('无限循环')
        # print(url,a)
        print(url1,b)
        print(headers1,proxies_1)
# print(ip)
# tianyancha(ip)
for i in range(10):
    # ge_ip=GetIP()
    # ip=ge_ip.get_random_ip()
    try:
        tianyancha()
    except Exception as e:
        print(e)
        continue
    time.sleep(3)
# get_ip(ip)