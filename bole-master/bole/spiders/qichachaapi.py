# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import requests
import time
import datetime,json
import random
from bole.items import QichachachaItem
from bole.utils.commmon import get_md5

class QichachaapiSpider(scrapy.Spider):
    name = 'qichachaapi'
    allowed_domains = ['qichacha.com']
    start_urls = ['http://qichacha.com/']
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
    custom_settings = {
        "COOKIES_ENABLED": False,#不发送cookies
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            # 'Cookie': 'UM_distinctid=1628aa341cf1a4-04b8862d9b155b-5d4e211f-1fa400-1628aa341d0457; _uab_collina=152274438996233822069572; hasShow=1; acw_tc=AQAAAJgFkQsueAsAp31xq80QhMfMiy/s; PHPSESSID=dhkook1e0jmobj3aloidf2ur70; _umdata=E2AE90FA4E0E42DE9EB61A4FD301DB7FB77437728CF6048AB82662AD7B79C81AFA7026403D2CAFBFCD43AD3E795C914C6D829DD7915A193E6231CC724DBA8E95; zg_did=%7B%22did%22%3A%20%221628aa342561b6-0be159c0165c3b-5d4e211f-1fa400-1628aa342573dc%22%7D; CNZZDATA1254842228=718863426-1522741815-https%253A%252F%252Fwww.baidu.com%252F%7C1525311824; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201525314210917%2C%22updated%22%3A%201525314746000%2C%22info%22%3A%201524728148709%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%2246ccf44740e63f076a8bb5c866706f14%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1525225145,1525242060,1525310810,1525311177; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1525314746',
            'Host': 'www.qichacha.com',
            'Upgrade - Insecure - Requests': '1',
            'Referer': 'https://www.baidu.com',
            'User-Agent': UA,
        }
    }
    def start_requests(self):
        while True:
            try:
                appid = '1787200360185404'
                now = datetime.datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                url = 'appid' + appid + 'timestamp' + timestamp.replace(' ', '') + 'keysecretG5FVJW76YFD72G16CI2VRMQP8ORWG20R'
                sign = get_md5(url)
                # print(appid, '\n',
                #       timestamp, '\n',
                #       sign)
                timestamp = timestamp.replace(' ', '%20')
                final_url = 'http://demo5.7gr.com.cn/api/company?appid={}&timestamp={}&sign={}'.format(appid, timestamp, sign)
                print(final_url)
                # b=urllib.parse.quote(' ')
                # print(b)
                web_data = requests.get(final_url).text
                xiangqing = json.loads(web_data)
                datas = xiangqing['data']
                for data in datas:
                    print(data['url'])
                    url=data['url']
                    id=data['id']
                    yield Request(url, self.parse_job,meta={'id':id})
            except:
                continue


    def parse_job(self, response):
        qichacha_item = QichachachaItem()
        # 网址
        url = response.url
        id=response.meta['id']
        # md5_url=get_md5(response.url)
        # 公司名称
        try:
            company = response.xpath('//div[@class="content"]/div[1]/h1/text()').extract_first().strip()
        except:
            company = response.xpath('//div[@class="content"]/div[1]/text()').extract_first().strip()
        # 公司电话
        dianhua=response.xpath('//div[@class="content"]/div[2]/span[1]/text()').extract_first().strip()
        if dianhua=='电话：':
            try:
                tel = response.xpath('//div[@class="content"]/div[2]/span[2]/span[1]/text()').extract_first().strip()
                email = response.xpath('//div[@class="content"]/div[3]/span[2]/a/text()').extract_first().strip()
                try:
                    www = response.xpath('//div[@class="content"]/div[3]/span[4]')[0].xpath('string(.)').extract_first().strip()
                except:
                    www = '暂无'
            except:
                tel = response.xpath('//div[@class="content"]/div[2]/span[2]/text()').extract_first().strip()
                # 公司邮箱
                email = response.xpath('//div[@class="content"]/div[3]/span[2]/text()').extract_first().strip()
                # 公司网址
                try:
                    www = response.xpath('//div[@class="content"]/div[3]/span[4]/text()').extract_first().strip()
                except:
                    www = '暂无'
        else:
            tel = response.xpath('//div[@class="content"]/div[3]/span[2]/text()').extract_first()
            if tel != '':
                # 公司邮箱
                email = response.xpath('//div[@class="content"]/div[4]/span[2]/text()').extract_first().strip()
                # 公司网址
                try:
                    www = response.xpath('//div[@class="content"]/div[4]/span[4]/text()').extract_first().strip()
                except:
                    www = '暂无'
            else:
                tel = response.xpath('//div[@class="content"]/div[3]/span[2]/span[1]/text()').extract_first().strip()
                email = response.xpath('//div[@class="content"]/div[4]/span[2]/a/text()').extract_first().strip()
                try:
                    www = response.xpath('//div[@class="content"]/div[4]/span[4]')[0].xpath('string(.)').extract_first().strip()
                except:
                    www = '暂无'

        leixing = response.xpath('//div[@class="logo"]/div[1]/@class').extract_first().strip()
        if leixing == 'c_logo_shzz':
            # print('社会组织')
            # 公司地址
            try:
                addr = response.xpath('//*[@id="Cominfo"]/table//tr[7]/td[2]/text()').extract_first().strip()
            except:
                addr = '-'
            # 法定代表人
            try:
                delegate = response.xpath('//*[@id="Cominfo"]/table//tr[2]/td[2]/text()').extract_first().strip()
            except:
                delegate = 'null'
            # 注册资本
            login_money = response.xpath('//*[@id="Cominfo"]/table//tr[2]/td[4]/text()').extract_first().strip()
            # 实交资本
            real_money = '-'
            # 经营状态
            status = response.xpath('//*[@id="Cominfo"]/table//tr[3]/td[4]/text()').extract_first().strip()
            # 成立日期
            login_time = response.xpath('//*[@id="Cominfo"]/table//tr[3]/td[2]/text()').extract_first().strip()
            # 工商注册号
            Registration = '-'
            # 组织结构代码
            org_number = '-'
            # 纳税人识别号
            taxpayer_number = '-'
            # 统一信用代码
            credit_number =  response.xpath('//*[@id="Cominfo"]/table//tr[1]/td[2]/text()').extract_first().strip()
            # 企业类型
            company_type =response.xpath('//*[@id="Cominfo"]/table//tr[4]/td[2]/text()').extract_first().strip()
            # 行业
            profession = response.xpath('//*[@id="Cominfo"]/table//tr[3]/td[2]/text()').extract_first().strip()
            # 核准日期
            approved_date = '-'
            # 登记机关
            registration_org = response.xpath('//*[@id="Cominfo"]/table//tr[4]/td[4]/text()').extract_first().strip()
            # 所属地区
            region = '-'
            # 英文名
            english_name = '-'
            # 曾用名
            old_name = '-'
            # 经营方式
            business_mode ='-'
            # 人员规模
            staff_size = '-'
            # 经营期限
            business_date = response.xpath('//*[@id="Cominfo"]/table//tr[5]/td[4]/text()').extract_first().strip()
            # 经营范围
            business_scope = response.xpath('//*[@id="Cominfo"]/table//tr[6]/td[2]/text()').extract_first().strip()
            # 股东信息
            partner_info = '-'
        else:
            # print('企业')
            # 公司地址
            try:
                addr = response.xpath('//*[@id="Cominfo"]/table[2]//tr[10]/td[2]/text()').extract_first().strip()
            except:
                addr = 'null'
            # 法定代表人
            try:
                delegate = response.xpath('//div[@class="boss-td"]/div[1]/div[2]/a[1]/text()').extract_first().strip()
                if not delegate:
                    delegate = response.xpath('//div[@class="boss-td"]/a[1]/text()').extract_first().strip().strip()
            except:
                delegate = 'null'
            # 注册资本
            login_money = response.xpath('//*[@id="Cominfo"]/table[2]//tr[1]/td[2]/text()').extract_first().strip()
            # 实交资本
            real_money = response.xpath('//*[@id="Cominfo"]/table[2]//tr[1]/td[4]/text()').extract_first().strip()
            # 经营状态
            status = response.xpath('//*[@id="Cominfo"]/table[2]//tr[2]/td[2]/text()').extract_first().strip()
            # 成立日期
            login_time = response.xpath('//*[@id="Cominfo"]/table[2]//tr[2]/td[4]/text()').extract_first().strip()
            # 工商注册号
            Registration = response.xpath('//*[@id="Cominfo"]/table[2]//tr[3]/td[2]/text()').extract_first().strip()
            # 组织结构代码
            org_number = response.xpath('//*[@id="Cominfo"]/table[2]//tr[3]/td[4]/text()').extract_first().strip()
            # 纳税人识别号
            taxpayer_number = response.xpath('//*[@id="Cominfo"]/table[2]//tr[4]/td[2]/text()').extract_first().strip()
            # 统一信用代码
            credit_number = response.xpath('//*[@id="Cominfo"]/table[2]//tr[4]/td[4]/text()').extract_first().strip()
            # 企业类型
            company_type = response.xpath('//*[@id="Cominfo"]/table[2]//tr[5]/td[2]/text()').extract_first().strip()
            # 行业
            profession = response.xpath('//*[@id="Cominfo"]/table[2]//tr[5]/td[4]/text()').extract_first().strip()
            # 核准日期
            approved_date = response.xpath('//*[@id="Cominfo"]/table[2]//tr[6]/td[2]/text()').extract_first().strip()
            # 登记机关
            registration_org = response.xpath('//*[@id="Cominfo"]/table[2]//tr[6]/td[4]/text()').extract_first().strip()
            # 所属地区
            region = response.xpath('//*[@id="Cominfo"]/table[2]//tr[7]/td[2]/text()').extract_first().strip()
            # 英文名
            english_name = response.xpath('//*[@id="Cominfo"]/table[2]//tr[7]/td[4]/text()').extract_first().strip()
            # 曾用名
            old_name = response.xpath('//*[@id="Cominfo"]/table[2]//tr[8]/td[2]/text()').extract_first().strip()
            # 经营方式
            business_mode = response.xpath('//*[@id="Cominfo"]/table[2]//tr[8]/td[4]/text()').extract_first().strip()
            # 人员规模
            staff_size = response.xpath('//*[@id="Cominfo"]/table[2]//tr[9]/td[2]/text()').extract_first().strip()
            # 经营期限
            business_date = response.xpath('//*[@id="Cominfo"]/table[2]//tr[9]/td[4]/text()').extract_first().strip()
            # 经营范围
            business_scope = response.xpath('//*[@id="Cominfo"]/table[2]//tr[11]/td[2]/text()').extract_first().strip()
            # 股东信息
            try:
                partner_info=[]
                #股东名字
                partner_names = response.xpath('//section[@id="Sockinfo"]//tr')
                for i in range(2,len(partner_names)+1):
                    try:
                        # print(i)
                        # 股东名字
                        partner_names_xpath=r'//section[@id="Sockinfo"]//tr[{}]/td[2]/a[1]'.format(i)
                        # print(partner_names_xpath)
                        partner_name = response.xpath(partner_names_xpath)[0].xpath('string(.)').extract_first().replace('\n','').replace(' ','')
                        print(partner_name)
                        #持股比例
                        partner_bilis_xpath=r'//section[@id="Sockinfo"]//tr[{}]/td[3]'.format(i)
                        partner_bili = response.xpath(partner_bilis_xpath)[0].xpath('string(.)').extract_first().replace('\n','').replace(' ','')
                        print(partner_bili)
                        #认缴出资
                        partner_chuzis_xpath = r'//section[@id="Sockinfo"]//tr[{}]/td[4]'.format(i)
                        partner_chuzi = response.xpath(partner_chuzis_xpath)[0].xpath('string(.)').extract_first().replace('\n','').replace(' ','')
                        # print(partner_chuzi)
                        # #认缴日期
                        partner_riqis_xpath = r'//section[@id="Sockinfo"]//tr[{}]/td[5]'.format(i)
                        partner_riqi = response.xpath(partner_riqis_xpath)[0].xpath('string(.)').extract_first().replace('\n','').replace(' ','')
                        # print(partner_riqi)
                        #股东类型
                        partner_leixings_xpath = r'//section[@id="Sockinfo"]//tr[{}]/td[6]'.format(i)
                        partner_leixing = response.xpath(partner_leixings_xpath)[0].xpath('string(.)').extract_first().replace('\n','').replace(' ','')
                        # print(partner_leixing)
                        dict={}
                        dict['mingzi']=partner_name.strip()
                        dict['chuzibili']=partner_bili.strip()
                        dict['chuzijine'] = partner_chuzi.strip()
                        dict['chuziriqi'] = partner_riqi.strip()
                        dict['gudongleixing'] = partner_leixing.strip()
                        partner_info.append(dict)
                    except:
                        continue
                a=partner_info[0]
            except:
                partner_info = ['-']
            # print(partner_info)
            #主要成员
            try:
                main_member=[]
                mainmember_names=response.xpath('//section[@id="Mainmember"]//tr/td[2]/a[1]/text()').extract()
                mainmember_zhiweis = response.xpath('//section[@id="Mainmember"]//tr/td[3]/text()').extract()
                for mainmember_name,mainmember_zhiwei in zip(mainmember_names,mainmember_zhiweis):
                    dict = {}
                    dict['name']=mainmember_name
                    dict['zhiwei'] = mainmember_zhiwei.strip()
                    main_member.append(dict)
                a = main_member[0]
                # print(main_member)
            except:
                main_member=['-']
            # 对外投资
            try:
                touzilist = []
                # 投资名字
                touzi_names = response.xpath('//section[@id="touzilist"]//tr')
                for i in range(2, len(touzi_names) + 1):
                    try:
                        # print(i)
                        # 被投资名字
                        touzi_names_xpath = r'//section[@id="touzilist"]//tr[{}]/td[1]/a[1]'.format(i)
                        # print(partner_names_xpath)
                        touzi_name = response.xpath(touzi_names_xpath)[0].xpath('string(.)').extract_first().replace('\n', '').replace(
                            ' ', '')
                        # print(touzi_name)
                        # 被投资法人
                        touzi_faren_xpath = r'//section[@id="touzilist"]//tr[{}]/td[2]/a[1]'.format(i)
                        touzi_faren = response.xpath(touzi_faren_xpath)[0].xpath('string(.)').extract_first().replace('\n', '').replace(
                            ' ', '')
                        # print(touzi_faren)
                        # 认缴出资
                        touzi_ziben_xpath = r'//section[@id="touzilist"]//tr[{}]/td[3]'.format(i)
                        touzi_ziben = response.xpath(touzi_ziben_xpath)[0].xpath('string(.)').extract_first().extract_first().replace('\n', '').replace(
                            ' ', '')
                        # print(touzi_ziben)
                        # 投资比例
                        touzi_bili_xpath = r'//section[@id="touzilist"]//tr[{}]/td[4]'.format(i)
                        touzi_bili = response.xpath(touzi_bili_xpath)[0].xpath('string(.)').extract_first().replace('\n', '').replace(
                            ' ', '')
                        # print(touzi_bili)
                        # 投资日期
                        touzi_riqi_xpath = r'//section[@id="touzilist"]//tr[{}]/td[5]'.format(i)
                        touzi_riqi = response.xpath(touzi_riqi_xpath)[0].xpath('string(.)').extract_first().replace('\n', '').replace(
                            ' ', '')
                        # print(touzi_riqi)
                        # 投资状态
                        touzi_zhuangtai_xpath = r'//section[@id="touzilist"]//tr[{}]/td[6]'.format(i)
                        touzi_zhuangtai = response.xpath(touzi_zhuangtai_xpath)[0].xpath('string(.)').extract_first().replace('\n',
                                                                                                          '').replace(
                            ' ', '')
                        # print(touzi_zhuangtai)
                        dict = {}
                        dict['beitouzimingcheng'] = touzi_name.strip()
                        dict['beitouzifaren'] = touzi_faren.strip()
                        dict['zhuceziben'] = touzi_ziben.strip()
                        dict['chuzibili'] = touzi_bili.strip()
                        dict['chengliriqi'] = touzi_riqi.strip()
                        dict['zhuangtai'] = touzi_zhuangtai.strip()
                        touzilist.append(dict)
                    except:
                        continue
                # print(touzilist)
                a = touzilist[0]
            except:
                touzilist=['-']
            # 对外投资
            # 分支机构
            try:
                fenzhilist = []
                # 分支名字
                fenzhi_names = response.xpath('//section[@id="Subcom"]//tr')
                print(len(fenzhi_names))
                for i in range(1, len(fenzhi_names) + 1):
                    try:
                        # print(i)
                        # 分支名字
                        fenzhi_name_xpath = r'//section[@id="Subcom"]//tr[{}]/td[2]'.format(i)
                        # print(partner_names_xpath)
                        fenzhi_name = response.xpath(fenzhi_name_xpath)[0].xpath('string(.)').extract_first().replace('\n', '').replace(
                            ' ', '')
                        print(fenzhi_name)
                        # 分支名字
                        fenzhi_faren_1_xpath = r'//section[@id="Subcom"]//tr[{}]/td[4]'.format(i)
                        fenzhi_faren_1 = response.xpath(fenzhi_faren_1_xpath)[0].xpath('string(.)').extract_first().replace('\n',
                                                                                                        '').replace(
                            ' ', '')
                        print(fenzhi_faren_1)

                        dict = {}
                        dict['fenzhi_name'] = fenzhi_name.strip()
                        dict['fenzhi_name'] = fenzhi_faren_1.strip()
                        fenzhilist.append(dict)
                    except:
                        continue
                # print(fenzhilist)
                a = fenzhilist[0]
            except:
                fenzhilist = ['-']

            # 变更记录
            try:
                changelist = []
                # 变更名字
                touzi_names = response.xpath('//section[@id="Changelist"]//tr')
                for i in range(2, len(touzi_names) + 1):
                    try:
                        # print(i)
                        # 变更日期
                        biangeng_riqi_xpath = r'//section[@id="Changelist"]//tr[{}]/td[2]'.format(i)
                        biangeng_riqi = response.xpath(biangeng_riqi_xpath)[0].xpath('string(.)').extract_first().replace('\n',
                                                                                                      '').replace(
                            ' ',
                            '')
                        # print(biangeng_riqi)
                        # 变更项目
                        biangeng_xiangmu_xpath = r'//section[@id="Changelist"]//tr[{}]/td[3]'.format(i)
                        biangeng_xiangmu = response.xpath(biangeng_xiangmu_xpath)[0].xpath('string(.)').extract_first().replace('\n',
                                                                                                            '').replace(
                            ' ',
                            '')
                        # print(biangeng_xiangmu)
                        # 变更前
                        biangeng_qian_xpath = r'//section[@id="Changelist"]//tr[{}]/td[4]'.format(i)
                        biangeng_qian = response.xpath(biangeng_qian_xpath)[0].xpath('string(.)').extract_first().replace('\n',
                                                                                                      '').replace(
                            ' ',
                            '')
                        # print(biangeng_qian)
                        # 投资比例
                        biangeng_hou_xpath = r'//section[@id="Changelist"]//tr[{}]/td[5]'.format(i)
                        biangeng_hou = response.xpath(biangeng_hou_xpath)[0].xpath('string(.)').extract_first().replace('\n',
                                                                                                    '').replace(' ',
                                                                                                                '')
                        # print(biangeng_hou)
                        dict = {}
                        dict['biangeng_riqi'] = biangeng_riqi.strip()
                        dict['biangeng_xiangmu'] = biangeng_xiangmu.strip()
                        dict['biangeng_qian'] = biangeng_qian.strip()
                        dict['biangeng_hou'] = biangeng_hou.strip()
                        changelist.append(dict)
                    except:
                        continue
                print(changelist)
                a = changelist[0]
            except:
                changelist = ['-']

        qichacha_item['url']=url
        # qichacha_item['md5_url']=md5_url
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
        qichacha_item['partner_info'] = str(partner_info)
        qichacha_item['main_member'] = str(main_member)
        qichacha_item['conpany_id'] = id
        qichacha_item['touzilist'] = str(touzilist)
        qichacha_item['fenzhilist'] = str(fenzhilist)
        qichacha_item['changelist'] = str(changelist)

        print(qichacha_item)
        # print(url,'公司名', company, '电话', tel, '邮箱', email, '网址', www, addr, delegate, login_money, real_money, status,
        #       login_time, Registration, org_number,
        #       taxpayer_number, credit_number, company_type, profession, approved_date, registration_org, region,
        #       english_name,
        #       old_name, business_mode, staff_size, business_date, business_scope, partner_info,id)
        return qichacha_item
