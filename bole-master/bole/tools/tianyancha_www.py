import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pymysql
import time

def change(number):
    list=[]
    for i in number:
        if i=='0':
            i='5'
        elif i=='1':
            i='7'
        elif i=='2':
            i='0'
        elif i=='3':
            i='9'
        elif i=='4':
            i='1'
        elif i=='5':
            i='2'
        elif i=='6':
            i='3'
        elif i=='7':
            i='6'
        elif i=='8':
            i='8'
        elif i=='9':
            i='4'
        elif i=='银':
            i='万'
        list.append(i)
    a=''
    change=a.join(list)
    return change
def tianyancha(url):
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        # 'Cookie':'YCID=65c17ff0362511e8af0407cb1a76e068; undefined=65c17ff0362511e8af0407cb1a76e068; ssuid=7651366445; RTYCID=900dc3faa48a4fcf8818f36b47133944; aliyungf_tc=AQAAAECnJSx0dgYAZNrq3R6uWg7xQpEl; csrfToken=3A7aGXkzp1GsDL7rJGIqM4CK; token=8e6dfd47978546d4aff502e43761a4c8; _utm=c255b3af39c54b65ad1354a08af9b95a; jsid=SEM-BAIDU-PP-SY-000257; bannerFlag=true; Hm_lvt_d5ceb643638c8ee5fbf79d207b00f07e=1522651024,1522652784,1522653158; Hm_lpvt_d5ceb643638c8ee5fbf79d207b00f07e=1522654019; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1522655201,1522655212,1522655219,1522656386; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1522656386',
        'Host':'m.tianyancha.com',
        'Referer':'https://www.baidu.com/link?url=VF8tL1Jp7A-nGcitAGcTZetpBo6C2RQKE3ypTVnwy-QdNT04twqoZo62P5CMGdRsGNyYBxNUOcCz2Q0sArhtYYf6fRzP6eqQzNwZf4pinyS&wd=&eqid=f72f7a7f0001417a000000055ac2f324',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'ndows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
    a= requests.get(url,headers=headers).content.decode('utf-8')
    print(a)
    html = etree.HTML(a)
    #公司名称
    company=html.xpath('//div[@class="position-rel"]/h1/text()')
    company_number=url.split('/')[-1]
    #公司电话
    tel=html.xpath('//div[@id="wap_header_top"]/div[2]/div[1]/span[2]/text()')
    if not tel:
        tel='空'
    #公司邮箱
    email=html.xpath('//div[@id="wap_header_top"]/div[2]/div[2]/span[2]/text()')
    if not email:
        email='空'
    #公司网址
    www=html.xpath('//div[@id="wap_header_top"]/div[2]/div[3]/a[1]/text()')
    if not www:
        www='空'
    #公司地址
    addr=html.xpath('//div[@class="content-container pb10"]/div[14]/span[2]/text()')[0]
    #法定代表人
    delegate=html.xpath('//div[@class="content-container pb10"]/div[1]/span[2]/a/text()')
    if not delegate:
        delegate='空'
    #经营状态
    status=html.xpath('//div[@class="content-container pb10"]/div[2]/span[2]/text()')
    if not status:
        status='空'
    #注册时间
    try:
        login_time=html.xpath('//div[@class="content-container pb10"]/div[3]/span[2]/text/text()')
        login_time=change(login_time[0])
    except:
        login_time='空'
    #注册资本
    try:
        login_money=html.xpath('//div[@class="content-container pb10"]/div[4]/span[2]/text/text()')
        login_money=change(login_money[0])
    except:
        login_money='空'
    #行业
    profession=html.xpath('//div[@class="content-container pb10"]/div[5]/span[2]/text()')
    if not profession:
        profession='空'
    #企业类型
    company_type=html.xpath('//div[@class="content-container pb10"]/div[6]/span[2]/text()')
    if not company_type:
        company_type='空'
    #工商注册号
    Registration=html.xpath('//div[@class="content-container pb10"]/div[7]/span[2]/text()')
    if not Registration:
        Registration='空'
    #组织结构代码
    org_number=html.xpath('//div[@class="content-container pb10"]/div[8]/span[2]/text()')
    if not org_number:
        org_number='空'
    #统一信用代码
    credit_number=html.xpath('//div[@class="content-container pb10"]/div[9]/span[2]/text()')
    if not credit_number:
        credit_number='空'
    #纳税人识别号
    taxpayer_number=html.xpath('//div[@class="content-container pb10"]/div[10]/span[2]/text()')
    if not taxpayer_number:
        tetaxpayer_numberl='空'
    #经营期限
    business_date=html.xpath('//div[@class="content-container pb10"]/div[11]/span[2]/text()')
    if not business_date:
        business_date='空'
    #核准日期
    try:
        approved_date=html.xpath('//div[@class="content-container pb10"]/div[12]/span[2]/text/text()')
        approved_date=change(approved_date[0])
    except:
        approved_date='空'
    #登记机关
    registration_org=html.xpath('//div[@class="content-container pb10"]/div[13]/span[2]/text()')
    if not registration_org:
        registration_org='空'
    #经营范围
    business_scope=html.xpath('//div[@class="content-container pb10"]/div[15]/span[2]/span/span[1]/div/text/text()')
    if not business_scope:
        business_scope='空'
    #股东信息
    partner_info=html.xpath('//div[@id="_container_holder"]/div[1]/div[1]')[0].xpath('string(.)')
    partner_info=(str(partner_info)).replace('下载APP查看','')

    print(company_number,company,tel,email,www,addr,status,delegate,login_time,login_money,profession,company_type,Registration,org_number,credit_number,taxpayer_number
          ,business_date,approved_date,registration_org,business_scope,partner_info)
    #链接数据库
    conn = pymysql.connect('localhost','root','liyuanhao9286A','lyh',charset='utf8',use_unicode = True)#mysql使用的是gbk，而python使用的是ut8，所以鼻血设定后两个参数，后一个参数为是否使用字符集
    #创建数据库浮标
    cursor = conn.cursor()
    # 设置需要插入的行的名称
    insert_sql = """
        insert into tianyancha(company,company_number,tel,email,www,addr,status,delegate,login_time,login_money,profession,company_type,Registration,org_number,credit_number,taxpayer_number
      ,business_date,approved_date,registration_org,business_scope,partner_info)
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(insert_sql,(company,company_number,tel,email,www,addr,status,delegate,login_time,login_money,profession,company_type,Registration,org_number,credit_number,taxpayer_number
      ,business_date,approved_date,registration_org,business_scope,partner_info))
    # 完成插入后提交
    conn.commit()
url = 'https://www.tianyancha.com/company/1620101786'
url1 = 'https://www.tianyancha.com/company/1188239370'
tianyancha(url)
# def get_url():
#     conn = pymysql.connect('localhost', 'root', 'liyuanhao9286A', 'lyh', charset='utf8',
#                            use_unicode=True)  # mysql使用的是gbk，而python使用的是ut8，所以鼻血设定后两个参数，后一个参数为是否使用字符集
#     # 创建数据库浮标
#     cursor = conn.cursor()
#     random_sql = """
#             SELECT url FROM company_url
#         """
#     cursor.execute(random_sql)
#     rows = cursor.fetchall()
#     list=[]
#     for row in rows:
#         print(row[0])
#         # try:
#         tianyancha(row[0])
#         # except Exception as e:
#         #     print(e)
#         #     list.append(row[0])
#         #     continue
#         # finally:
#         #     time.sleep(3)
#
# get_url()