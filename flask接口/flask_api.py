from flask import Flask,jsonify,request
import requests
import pymysql.cursors
from lxml import etree
import random
from flask.ext.cache import Cache

conn = pymysql.connect('39.104.62.136', 'root', '*****', 'lyh', charset='utf8',use_unicode=True)
cursor = conn.cursor()

app = Flask(__name__)#创建一个服务，赋值给APP
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.config['JSON_AS_ASCII'] = False
@app.route('/get_user',methods=['post','get'])#指定接口访问的路径，支持什么请求方式get，post
#请求后直接拼接入参方式
@cache.cached(timeout=60*60*24)
def get_users():
    url = request.args.get('url')#使用request.args.get方式获取拼接的入参数据
    print(url)
    try:
      url=url.replace('https','http')
    except:
        pass
    if 'firm' not in url:
        return 'URL参数错误'
    print(url)
    while 1:
        try:
            ip = get_random_ip()
            proxies = {"http": ip, }
            print(url, ip)
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
            headers={
                'Host': 'www.qichacha.com',
                'User-Agent': UA,
            }
            a=requests.get(url,proxies=proxies,headers=headers,timeout=1).text
            # print(a)
            qichacha_item={}
            html=etree.HTML(a)
            # 公司名称
            try:
                company = html.xpath('//div[@class="content"]/div[1]/h1/text()')[0].strip()
            except:
                company = html.xpath('//div[@class="content"]/div[1]/text()')[0].strip()
            # 公司电话
            dianhua = html.xpath('//div[@class="content"]/div[2]/span[1]/text()')[0].strip()
            if dianhua == '电话：':
                try:
                    tel = html.xpath(
                        '//div[@class="content"]/div[2]/span[2]/span[1]/text()')[0].strip()
                    email = html.xpath('//div[@class="content"]/div[3]/span[2]/a/text()')[0].strip()
                    try:
                        www = html.xpath('//div[@class="content"]/div[3]/span[4]/text()')[0].strip()
                    except:
                        www = '暂无'
                except:
                    tel = html.xpath('//div[@class="content"]/div[2]/span[2]/text()')[0].strip()
                    # 公司邮箱
                    email = html.xpath('//div[@class="content"]/div[3]/span[2]/text()')[0].strip()
                    # 公司网址
                    try:
                        www = html.xpath('//div[@class="content"]/div[3]/span[4]/text()')[0].strip()
                    except:
                        www = '暂无'
            else:
                tel = html.xpath('//div[@class="content"]/div[3]/span[2]/text()')[0].strip()
                if tel != '':
                    # 公司邮箱
                    email = html.xpath('//div[@class="content"]/div[4]/span[2]/text()')[0].strip()
                    # 公司网址
                    try:
                        www = html.xpath('//div[@class="content"]/div[4]/span[4]/text()')[0].strip()
                    except:
                        www = '暂无'
                else:
                    tel = html.xpath(
                        '//div[@class="content"]/div[3]/span[2]/span[1]/text()')[0].strip()
                    email = html.xpath('//div[@class="content"]/div[4]/span[2]/a/text()')[0].strip()
                    try:
                        www = html.xpath('//div[@class="content"]/div[4]/span[4]')[0].xpath(
                            'string(.)')[0].strip()
                    except:
                        www = '暂无'
            leixing = html.xpath('//div[@class="logo"]/div[1]/@class')[0].strip()
            if leixing == 'c_logo_shzz':
                print('社会组织')
                # 公司地址
                try:
                    addr = html.xpath('//*[@id="Cominfo"]/table//tr[7]/td[2]/text()')[0].strip()
                except:
                    addr = 'null'
                # 法定代表人
                try:
                    delegate = html.xpath('//*[@id="Cominfo"]/table//tr[2]/td[2]/text()')[0].strip()
                except:
                    delegate = 'null'
                # 注册资本
                login_money = html.xpath('//*[@id="Cominfo"]/table//tr[2]/td[4]/text()')[0].strip()
                # 实交资本
                real_money = ''
                # 经营状态
                status = html.xpath('//*[@id="Cominfo"]/table//tr[3]/td[4]/text()')[0].strip()
                # 成立日期
                login_time = html.xpath('//*[@id="Cominfo"]/table//tr[3]/td[2]/text()')[0].strip()
                # 工商注册号
                Registration = ''
                # 组织结构代码
                org_number = ''
                # 纳税人识别号
                taxpayer_number = ''
                # 统一信用代码
                credit_number = html.xpath('//*[@id="Cominfo"]/table//tr[1]/td[2]/text()')[0].strip()
                # 企业类型
                company_type = html.xpath('//*[@id="Cominfo"]/table//tr[4]/td[2]/text()')[0].strip()
                # 行业
                profession = ''
                # 核准日期
                approved_date = ''
                # 登记机关
                registration_org = html.xpath('//*[@id="Cominfo"]/table//tr[4]/td[4]/text()')[0].strip()
                # 所属地区
                region = ''
                # 英文名
                english_name = ''
                # 曾用名
                old_name = ''
                # 经营方式
                business_mode = ''
                # 人员规模
                staff_size = ''
                # 经营期限
                business_date = html.xpath('//*[@id="Cominfo"]/table//tr[5]/td[4]/text()')[0].strip()
                # 经营范围
                business_scope = html.xpath('//*[@id="Cominfo"]/table//tr[6]/td[2]/text()')[0].strip()
                # 股东信息
                partner_info = ''
                print(url, '公司名', company, '电话', tel, '邮箱', email, '网址', www, addr, delegate, login_money, real_money,
                      status,
                      login_time, Registration, org_number,
                      taxpayer_number, credit_number, company_type, profession, approved_date, registration_org, region,
                      english_name,
                      old_name, business_mode, staff_size, business_date, business_scope, partner_info)
            else:
                print('企业')
                # 公司地址
                try:
                    addr = html.xpath('//*[@id="Cominfo"]/table[2]//tr[10]/td[2]/text()')[0].strip()
                except:
                    addr = 'null'
                # 法定代表人
                try:
                    delegate = html.xpath('//div[@class="boss-td"]/div[1]/div[2]/a[1]/text()')[0].strip()
                    if not delegate:
                        delegate = html.xpath('//div[@class="boss-td"]/a[1]/text()')[0].strip()
                except:
                    delegate = 'null'
                # 注册资本
                login_money = html.xpath('//*[@id="Cominfo"]/table[2]//tr[1]/td[2]/text()')[0].strip()
                # 实交资本
                real_money = html.xpath('//*[@id="Cominfo"]/table[2]//tr[1]/td[4]/text()')[0].strip()
                # 经营状态
                status = html.xpath('//*[@id="Cominfo"]/table[2]//tr[2]/td[2]/text()')[0].strip()
                # 成立日期
                login_time = html.xpath('//*[@id="Cominfo"]/table[2]//tr[2]/td[4]/text()')[0].strip()
                # 工商注册号
                Registration = html.xpath('//*[@id="Cominfo"]/table[2]//tr[3]/td[2]/text()')[0].strip()
                # 组织结构代码
                org_number = html.xpath('//*[@id="Cominfo"]/table[2]//tr[3]/td[4]/text()')[0].strip()
                # 纳税人识别号
                taxpayer_number = html.xpath('//*[@id="Cominfo"]/table[2]//tr[4]/td[2]/text()')[0].strip()
                # 统一信用代码
                credit_number = html.xpath('//*[@id="Cominfo"]/table[2]//tr[4]/td[4]/text()')[0].strip()
                # 企业类型
                company_type = html.xpath('//*[@id="Cominfo"]/table[2]//tr[5]/td[2]/text()')[0].strip()
                # 行业
                profession = html.xpath('//*[@id="Cominfo"]/table[2]//tr[5]/td[4]/text()')[0].strip()
                # 核准日期
                approved_date = html.xpath('//*[@id="Cominfo"]/table[2]//tr[6]/td[2]/text()')[0].strip()
                # 登记机关
                registration_org = html.xpath('//*[@id="Cominfo"]/table[2]//tr[6]/td[4]/text()')[0].strip()
                # 所属地区
                region = html.xpath('//*[@id="Cominfo"]/table[2]//tr[7]/td[2]/text()')[0].strip()
                # 英文名
                english_name = html.xpath('//*[@id="Cominfo"]/table[2]//tr[7]/td[4]/text()')[0].strip()
                # 曾用名
                old_name = html.xpath('//*[@id="Cominfo"]/table[2]//tr[8]/td[2]/text()')[0].strip()
                # 经营方式
                business_mode = html.xpath('//*[@id="Cominfo"]/table[2]//tr[8]/td[4]/text()')[0].strip()
                # 人员规模
                staff_size = html.xpath('//*[@id="Cominfo"]/table[2]//tr[9]/td[2]/text()')[0].strip()
                # 经营期限
                business_date = html.xpath('//*[@id="Cominfo"]/table[2]//tr[9]/td[4]/text()')[0].strip()
                # 经营范围
                business_scope = html.xpath('//*[@id="Cominfo"]/table[2]//tr[11]/td[2]/text()')[0].strip()
                # 股东信息
                try:
                    partner_infos = html.xpath('//*[@id="Sockinfo"]/table/tr')
                    partner_info = []
                    for i in partner_infos:
                        b = i.xpath('string(.)').replace('\n', '|').replace(' ', '')
                        partner_info.append(b)
                except:
                    partner_info = 'null'
            qichacha_item['url'] = url
            qichacha_item['company'] = company
            qichacha_item['tel'] = tel
            qichacha_item['email'] = email
            qichacha_item['www'] = www
            qichacha_item['addr'] = addr
            qichacha_item['delegate'] = delegate
            qichacha_item['login_money'] = login_money
            qichacha_item['real_money'] = real_money
            qichacha_item['status'] = status
            qichacha_item['login_time'] = login_time
            qichacha_item['Registration'] = Registration
            qichacha_item['org_number'] = org_number
            qichacha_item['taxpayer_number'] = taxpayer_number
            qichacha_item['credit_number'] = credit_number
            qichacha_item['company_type'] = company_type
            qichacha_item['profession'] = profession
            qichacha_item['approved_date'] = approved_date
            qichacha_item['registration_org'] = registration_org
            qichacha_item['region'] = region
            qichacha_item['english_name'] = english_name
            qichacha_item['old_name'] = old_name
            qichacha_item['business_mode'] = business_mode
            qichacha_item['staff_size'] = staff_size
            qichacha_item['business_date'] = business_date
            qichacha_item['business_scope'] = business_scope
            qichacha_item['partner_info'] = partner_info
            print(qichacha_item)
            i=1
            return jsonify(qichacha_item)
            break
        except Exception as e:
            print(e)
            continue
    # return '失败'

	#如果不在的话，返回err对应key的value转成的json串信息
@app.route('/home',methods=['post','get'])
def home():
    return '<h1>Home</h1>'

def get_random_ip():
    with open(r'E:\bole-master\bole\utils\proxies.txt', 'r') as f:
        proxies = f.readlines()
    proxy = random.choice(proxies).strip()
    print(proxy)
    return proxy
    # #从数据库中随机获取一个可用的ip
    # random_sql = """
    #       SELECT ip FROM proxy_ip
    #     ORDER BY RAND()
    #     LIMIT 1
    #     """
    # result = cursor.execute(random_sql)
    # for ip_info in cursor.fetchall():
    #     ip = ip_info[0]
    #     print("http://{0}".format(ip))
    #     return "http://{0}".format(ip)

app.run(host='0.0.0.0',port=****,debug=True,threaded=True)

# app.run(processes=3) processes 进程数量
#这个host：windows就一个网卡，可以不写，而liux有多个网卡，写成0:0:0可以接受任意网卡信息,
 # 通过访问127.0.0.1:8802/get_user，可返回data信息
#debug:调试的时候，可以指定debug=true；如果是提供接口给他人使用的时候，debug要去掉