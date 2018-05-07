# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bole.items import QichachachaItem
from bole.utils.commmon import get_md5
from scrapy_redis.spiders import RedisCrawlSpider
import random

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['qichacha.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        # 'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        # 'Cookie':'YCID=65c17ff0362511e8af0407cb1a76e068; undefined=65c17ff0362511e8af0407cb1a76e068; ssuid=7651366445; RTYCID=900dc3faa48a4fcf8818f36b47133944; aliyungf_tc=AQAAAECnJSx0dgYAZNrq3R6uWg7xQpEl; csrfToken=3A7aGXkzp1GsDL7rJGIqM4CK; token=8e6dfd47978546d4aff502e43761a4c8; _utm=c255b3af39c54b65ad1354a08af9b95a; jsid=SEM-BAIDU-PP-SY-000257; bannerFlag=true; Hm_lvt_d5ceb643638c8ee5fbf79d207b00f07e=1522651024,1522652784,1522653158; Hm_lpvt_d5ceb643638c8ee5fbf79d207b00f07e=1522654019; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1522655201,1522655212,1522655219,1522656386; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1522656386',
        # 'Host': 'www.qichacha.com',
        # 'Referer': 'http://www.qichacha.com/',
        'Upgrade-Insecure-Requests': '1',
        }
    }

    def start_requests(self):
        chengshi_list = [
            "/g_AH",
            "/g_BJ",
            "/g_CQ",
            "/g_FJ",
            "/g_GS",
            "/g_GD",
            "/g_GX",
            "/g_GZ",
            "/g_HAIN",
            "/g_HB",
            "/g_HLJ",
            "/g_HEN",
            "/g_HUB",
            "/g_HUN",
            "/g_JS",
            "/g_JX",
            "/g_JL",
            "/g_LN",
            "/g_NMG",
            "/g_NX",
            "/g_QH",
            "/g_SD",
            "/g_SH",
            "/g_SX",
            "/g_SAX",
            "/g_SC",
            "/g_TJ",
            "/g_XJ",
            "/g_XZ",
            "/g_YN",
            "/g_ZJ",
            "/g_CN", ]
        for chengshi in chengshi_list:
            base_url = 'https://fj.qichacha.com{}_'.format(chengshi)
            for i in range(1,2):
                url = base_url+str(i)+'.html'
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self,response):
        urls=response.xpath('//*[@id="searchlist"]/a[1]/@href').extract()
        for url in urls:
            print(url)
            final_url='https://fj.qichacha.com{}'.format(url)
            print(final_url)
            yield scrapy.Request(url=final_url, callback=self.parse_yemian, dont_filter=True)
    set=set()
    def parse_yemian(self,response):
        urls=response.xpath('//html/body/div[2]/div/div[2]/section[4]/ul/a/@href').extract()
        for url in urls:
            final_url = 'https://fj.qichacha.com{}'.format(url)
            yield scrapy.Request(url=final_url, callback=self.parse_yemian, dont_filter=True)
        qichacha_item = QichachachaItem()
        # 网址
        url = response.url
        md5_url = get_md5(response.url)
        self.set.add(md5_url)
        # 公司名称
        try:
            company = response.xpath('//div[@class="content"]/div[1]/h1/text()').extract_first().strip()
        except:
            company = response.xpath('//div[@class="content"]/div[1]/text()').extract_first().strip()
        # 公司电话
        dianhua = response.xpath('//div[@class="content"]/div[2]/span[1]/text()').extract_first().strip()
        if dianhua == '电话：':
            try:
                tel = response.xpath('//div[@class="content"]/div[2]/span[2]/span[1]/text()').extract_first().strip()
                email = response.xpath('//div[@class="content"]/div[3]/span[2]/a/text()').extract_first().strip()
                try:
                    www = response.xpath('//div[@class="content"]/div[3]/span[4]')[0].xpath(
                        'string(.)').extract_first().strip()
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
                    www = response.xpath('//div[@class="content"]/div[4]/span[4]')[0].xpath(
                        'string(.)').extract_first().strip()
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
            partner_info = a.join(partner_info).replace('\n', '|').replace(' ', '')
        except:
            partner_info = 'null'
        qichacha_item['url'] = url
        qichacha_item['md5_url'] = md5_url
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
        print('公司名', company, '电话', tel, '邮箱', email, '网址', www, addr, delegate, login_money, real_money, status,
              login_time, Registration, org_number,
              taxpayer_number, credit_number, company_type, profession, approved_date, registration_org, region,
              english_name,
              old_name, business_mode, staff_size, business_date, business_scope, partner_info)
        yield  qichacha_item

