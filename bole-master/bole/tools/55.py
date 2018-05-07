import requests
from lxml import etree
from bs4 import BeautifulSoup
import pymysql
import random
import time
from bole.utils.ip import GetIP
def tianyancha(url):
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
    get_ip = GetIP()
    ip=get_ip.get_random_ip()
    proxies = {"http": ip,}
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        # 'Cookie':'YCID=65c17ff0362511e8af0407cb1a76e068; undefined=65c17ff0362511e8af0407cb1a76e068; ssuid=7651366445; RTYCID=900dc3faa48a4fcf8818f36b47133944; aliyungf_tc=AQAAAECnJSx0dgYAZNrq3R6uWg7xQpEl; csrfToken=3A7aGXkzp1GsDL7rJGIqM4CK; token=8e6dfd47978546d4aff502e43761a4c8; _utm=c255b3af39c54b65ad1354a08af9b95a; jsid=SEM-BAIDU-PP-SY-000257; bannerFlag=true; Hm_lvt_d5ceb643638c8ee5fbf79d207b00f07e=1522651024,1522652784,1522653158; Hm_lpvt_d5ceb643638c8ee5fbf79d207b00f07e=1522654019; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1522655201,1522655212,1522655219,1522656386; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1522656386',
        'Host':'www.qichacha.com',
        'Referer':'http://www.qichacha.com/index_verify?type=companyview&back=/firm_2787fef1343ce37a36df1cef965abe1c.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':UA,
        }
    b=requests.get(url,headers=headers,proxies=proxies)
    print(ip,b.headers)
    a= requests.get(url,headers=headers,proxies=proxies).content.decode('utf-8')
    print(url,a)
    html = etree.HTML(a)
    #网址
    url=url
    #公司名称
    try:
        company=html.xpath('//div[@class="content"]/div[1]/h1/text()')[0].strip()
    except:
        company = html.xpath('//div[@class="content"]/div[1]/text()')[0].strip()
    #公司电话
    tel=html.xpath('//div[@class="content"]/div[2]/span[2]/text()')[0].strip()
    if tel:
        #公司邮箱
        email=html.xpath('//div[@class="content"]/div[3]/span[2]/text()')
        #公司网址
        try:
            www=html.xpath('//div[@class="content"]/div[3]/span[4]')[0].xpath('string(.)')
        except:
            www='暂无'
    if not tel:
        tel=html.xpath('//div[@class="content"]/div[2]/span[2]/span[1]/text()')
        email=html.xpath('//div[@class="content"]/div[3]/span[2]/a/text()')
        try:
            www=html.xpath('//div[@class="content"]/div[3]/span[4]')[0].xpath('string(.)')
        except:
            www='暂无'
    #公司地址
    try:
        addr=html.xpath('//*[@id="Cominfo"]/table[2]//tr[10]/td[2]/text()')[0].strip()
    except:
        addr='null'
    #法定代表人
    try:
        delegate=html.xpath('//div[@class="boss-td"]/div[1]/div[2]/a[1]/text()')
        if not delegate:
            delegate=html.xpath('//div[@class="boss-td"]/a[1]/text()')
    except:
        delegate='null'
    # if not delegate:
    #     delegate='空'
    #注册资本
    login_money=html.xpath('//*[@id="Cominfo"]/table[2]//tr[1]/td[2]/text()')[0].strip()
    #实交资本
    real_money=html.xpath('//*[@id="Cominfo"]/table[2]//tr[1]/td[4]/text()')[0].strip()
    #经营状态
    status=html.xpath('//*[@id="Cominfo"]/table[2]//tr[2]/td[2]/text()')[0].strip()
    # if not status:scrapy rules怎么提取只有后半部分的的网址？
    #     status='空'
    #成立日期
    login_time=html.xpath('//*[@id="Cominfo"]/table[2]//tr[2]/td[4]/text()')[0].strip()
    #工商注册号
    Registration=html.xpath('//*[@id="Cominfo"]/table[2]//tr[3]/td[2]/text()')[0].strip()
    # if not Registration:
    #     Registration='空'
    #组织结构代码
    org_number=html.xpath('//*[@id="Cominfo"]/table[2]//tr[3]/td[4]/text()')[0].strip()
    # if not org_number:
    #     org_number='空'
    #纳税人识别号
    taxpayer_number=html.xpath('//*[@id="Cominfo"]/table[2]//tr[4]/td[2]/text()')[0].strip()
    # if not taxpayer_number:
    #     tetaxpayer_numberl='空'
    #统一信用代码
    credit_number=html.xpath('//*[@id="Cominfo"]/table[2]//tr[4]/td[4]/text()')[0].strip()
    # if not credit_number:
    #     credit_number='空'
    #企业类型
    company_type=html.xpath('//*[@id="Cominfo"]/table[2]//tr[5]/td[2]/text()')[0].strip()
    # if not company_type:
    #     company_type='空'
    #行业
    profession=html.xpath('//*[@id="Cominfo"]/table[2]//tr[5]/td[4]/text()')[0].strip()
    # if not profession:
    #     profession='空'
    #核准日期
    try:
        approved_date=html.xpath('//*[@id="Cominfo"]/table[2]//tr[6]/td[2]/text()')[0].strip()
    except:
        approved_date='空'
    #登记机关
    registration_org=html.xpath('//*[@id="Cominfo"]/table[2]//tr[6]/td[4]/text()')[0].strip()
    # if not registration_org:
    #     registration_org='空'
    #所属地区
    region=html.xpath('//*[@id="Cominfo"]/table[2]//tr[7]/td[2]/text()')[0].strip()
    #英文名
    english_name=html.xpath('//*[@id="Cominfo"]/table[2]//tr[7]/td[4]/text()')[0].strip()
    #曾用名
    old_name=html.xpath('//*[@id="Cominfo"]/table[2]//tr[8]/td[2]/text()')[0].strip()
    #经营方式
    business_mode=html.xpath('//*[@id="Cominfo"]/table[2]//tr[8]/td[4]/text()')[0].strip()
    #人员规模
    staff_size=html.xpath('//*[@id="Cominfo"]/table[2]//tr[9]/td[2]/text()')[0].strip()
    #经营期限
    business_date=html.xpath('//*[@id="Cominfo"]/table[2]//tr[9]/td[4]/text()')[0].strip()
    #经营范围
    business_scope=html.xpath('//*[@id="Cominfo"]/table[2]//tr[11]/td[2]/text()')[0].strip()
    #股东信息
    try:
        partner_info=str(html.xpath('//*[@id="Sockinfo"]/table')[0].xpath('string(.)')).replace('\n','|').replace(' ','')
    except:
        partner_info='null'
    print('公司名',company,'电话',tel,'邮箱',email,'网址',www,addr,delegate,login_money,real_money,status,login_time,Registration,org_number,
          taxpayer_number,credit_number,company_type,profession,approved_date,registration_org,region,english_name,
          old_name,business_mode,staff_size,business_date,business_scope,partner_info)
url='http://fj.qichacha.com/firm_20708af4c7e049a334b4a9fb12b3edd3.html'
tianyancha(url)
