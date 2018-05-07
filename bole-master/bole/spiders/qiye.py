# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bole.scrapy_redis.spiders import RedisCrawlSpider
from bole.items import QichachachaItem
from bole.utils.commmon import get_md5
import random


class QiyeSpider(RedisCrawlSpider):
    name = 'qiye'
    allowed_domains = ['qichacha.com']
    start_urls = ['http://fj.qichacha.com/g_AH.html']
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
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Connection': 'keep-alive',
            # 'Cookie': 'user_trace_token=20171015132411-12af3b52-3a51-466f-bfae-a98fc96b4f90; LGUID=20171015132412-13eaf40f-b169-11e7-960b-525400f775ce; SEARCH_ID=070e82cdbbc04cc8b97710c2c0159ce1; ab_test_random_num=0; X_HTTP_TOKEN=d1cf855aacf760c3965ee017e0d3eb96; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsXIrWUxpNGLE2g_bKzlUCXPTRJMHxfCs6L20RqgCpUq%26wd%3D%26eqid%3Dee53adaf00026e940000000559e354cc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotjob; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG50060B788C4EED616EB9D1BF30380575; _gat=1; _ga=GA1.2.471681568.1508045060; LGSID=20171015203008-94e1afa5-b1a4-11e7-9788-525400f775ce; LGRID=20171015204552-c792b887-b1a6-11e7-9788-525400f775ce',
            'Host': 'www.qichacha.com',
            # 'Origin': 'https://www.lagou.com',
            # 'Referer': 'https://www.lagou.com/',
            'User-Agent': UA,
        }
    }
    rules = (
        Rule(LinkExtractor(allow=(r'g_.*?.html',)), follow=True),  # 跟踪符合规则的网址
        Rule(LinkExtractor(allow=(r'firm_.*?.html')), callback='parse_job', follow=True,process_links = 'link_filtering'),
    )
    def link_filtering(self, links):
                ret = []
                for link in links:
                    # link.url=link.url.replace('https','http')
                    print(link.url)
                    # url = link.url
                    # final_url=url.replace('https','http')
                    # print(url,final_url)
                # print(links)
                return links
    def parse_job(self, response):
        qichacha_item = QichachachaItem()
        # 网址
        url = response.url
        md5_url=get_md5(response.url)
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
            partner_info = response.xpath('//*[@id="Sockinfo"]/table/tr').xpath('string(.)').extract()
            a = ''
            partner_info=a.join(partner_info).replace('\n', '|').replace(' ', '')
        except:
            partner_info = 'null'
        qichacha_item['url']=url
        qichacha_item['md5_url']=md5_url
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
        print(url,'公司名', company, '电话', tel, '邮箱', email, '网址', www, addr, delegate, login_money, real_money, status,
              login_time, Registration, org_number,
              taxpayer_number, credit_number, company_type, profession, approved_date, registration_org, region,
              english_name,
              old_name, business_mode, staff_size, business_date, business_scope, partner_info)
        return qichacha_item

