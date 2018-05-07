# 天机查项目

抓取企查查无需登录的工商信息，保存在mysql，或存入redis队列，并提供api接口用于手动更新。

## 使用crawlspider爬取企查查
由于企查查没有网站地图，但是有根据地方分组的企业信息，每个省份有500组，但是全部的数据却有9500万，这个数量是远远不够的。所以最初的策略是抓取
这些地方的企业信息，然后获取企业相详情页面下方的你感兴趣的企业，扩展地图。并且使用布隆过滤器按位去重，并使用redis实现持久化和分布式。

## 设置提取规则
使用scrapy的crawlspider全站爬虫爬取企查查，设置好start_urls,和headers。并且禁用cookies,和现在间隔。然后设置爬取规则，并且将企业信息页交由parse_job处理。从而遍历所有的简历页面。
```
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
```


## 使用parse_job提取标签并在并存入item

使用css和xpath提取页面标签信息，qichacha_item，并交给pipelines下载。

```
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
```
## 在items中设置好所需要提取的信息，并且在middlewares.py中设置好代理ip和重试。

### 设置item

```
    def parse_job(self, response):
        # 解析拉勾网的职位
        item_loader = LagouJobItemLoader(item= LagouJobItem(),response = response)#itemloder传入item和response
        item_loader.add_css('title','.job-name::attr(title)')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',get_md5(response.url))
        item_loader.add_css('salary','.job_request p .salary::text')
        item_loader.add_xpath('job_city','//*[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath('work_years', '//*[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath('degree_need', '//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath('job_type', '//*[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css('tags','.position-label li::text')
        item_loader.add_css('publish_time','.publish_time::text')
        item_loader.add_css('job_advantage','.job-advantage p::text')
        item_loader.add_css('job_desc','.job_bt div')
        item_loader.add_css('job_addr', '.work_addr')
        item_loader.add_css('company_name', '.job_company a img::attr(alt)')
        item_loader.add_css('company_url', '.job_company a::attr(href)')
        item_loader.add_value('crawl_time',datetime.now())
        a = item_loader
        job_item = item_loader.load_item()

        return job_item
```

### 设置随机请求头

```
    class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    def __init__(self,crawler):
        super(RandomUserAgentMiddlware,self).__init__()#super的作用是获取父类的初始方法，这里是获取一个类方法
        self.ua = UserAgent()#这里是引进的一个随机UA的模块
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)#获取crawler，其中包括setting

    def process_request(self,request,spider):
        # print(request.headers)
        def get_ua():
            return getattr(self.ua,self.ua_type)#getattr函数可以根据传递的后边参数的不同，获取前边函数的不同值方法，类似与'.'
        random_ua = get_ua()
        request.headers.setdefault('User_Agent',random_ua)
```

### 设置动态ip代理
由于频繁访问mysql容易造成堵塞，所以将ip存储在本地。

```
   class RandomProxyMiddleware(object):
    # #使用异步化接口提取IP，否则会造成堵塞。
    # def __init__(self, dbpool):
    #     self.dbpool = dbpool
    #
    # @classmethod
    # def from_settings(cls, settings):  # 调用settings值的固定函数，调用方法和字典一样
    #     # 将参数字典化方便传入
    #     dbparms = dict(
    #         host=settings['MYSQL_HOST'],
    #         db=settings['MYSQL_DBNAME'],
    #         user=settings['MYSQL_USER'],
    #         passwd=settings['MYSQL_PASSWD'],
    #         charset='utf8',
    #         cursorclass=pymysql.cursors.DictCursor,
    #         use_unicode=True,
    #
    #     )
    #     # from twisted.enterprise import adbapi  Twisted为数据库提供的一个异步化接口。
    #     dbpool = adbapi.ConnectionPool('pymysql', **dbparms)  # 第一个是需要的函数名称，后边是不定长的字典参数
    #     return cls(dbpool)
    #
    # def process_request(self, request, spider):
    #     # 使用twisted将mysql读取变成异步执行
    #     query = self.dbpool.runInteraction(self.get_random_ip, request)
    #     query.addErrback(self.handle_error)  # 处理异常
    #
    # def handle_error(self, failure):
    #     # 处理异步插入异常
    #     print(failure)
    #
    # def get_random_ip(self, cursor, request):
    #     # 从数据库中随机获取一个可用的ip
    #     random_sql = """
    #           SELECT ip FROM proxy_ip
    #         ORDER BY RAND()
    #         LIMIT 1
    #         """
    #     result = cursor.execute(random_sql)
    #     for ip_info in cursor.fetchall():
    #         ip = ip_info['ip']
    #         print("http://{0}".format(ip))
    #         request.meta["proxy"] = "http://{0}".format(ip)
    #         # cursor.commit()
    #动态设置ip代理
    def process_request(self, request, spider):
        while True:
            try:
                with open(r'E:\bole-master\bole\utils\proxies.txt', 'r') as f:
                    proxies = f.readlines()
                proxy = random.choice(proxies).strip()
                print(proxy)
                # request.headers.setdefault('Host', 'www.qichacha.com')
                request.meta["proxy"] = proxy
                break
            except:
                time.sleep(1)
                continue
```

### 设置重试机制
在获取页面时，返回不正确验证码，或验证码时重新获取一次。

### 在setting中设置:
```

RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404,405, 408]#重试状态码
RETRY_TIMES = 500#设置重试次数

```
### 在middlewares中设置:
```
   class LocalRetryMiddleware(RetryMiddleware):
    #重试设置，如果代理IP请求异常则重新获取。
    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        # 如果URL中没有firm，则不进行下面的操作。
        if 'firm' in response.url:
            try:
                login_money = response.xpath('//*[@id="Cominfo"]/table[2]//tr[1]/td[2]/text()').extract_first().strip()
            except Exception as e:
                reason=e
                #下方为返回重试
                return self._retry(request, reason, spider) or response
        return response
```

## 最后使用pipelines把信息储存在mysql中，或放入redis队列。
使用twisted的mysql异步接口将信息储存在mysql中。
```
class QiyeTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):#调用settings值的固定函数，调用方法和字典一样
        # 将参数字典化方便传入
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset= 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,

        )
        # from twisted.enterprise import adbapi  Twisted为数据库提供的一个异步化接口。
        dbpool = adbapi.ConnectionPool('pymysql',**dbparms)#第一个是需要的函数名称，后边是不定长的字典参数

        return  cls(dbpool)
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)#处理异常

    def handle_error(self,failure):
        #处理异步插入异常
        print(failure)
    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into qichacha_zuixin(url,conpany_id,company,tel,email,www,addr,delegate,login_money,real_money,status,login_time,Registration,org_number,
                          taxpayer_number,credit_number,company_type,profession,approved_date,registration_org,region,english_name,
                          old_name,business_mode,staff_size,business_date,business_scope,partner_info,main_member,touzilist,fenzhilist,changelist)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql,(item['url'],item['conpany_id'],item['company'],item['tel'],item['email'],item['www'],item['addr'],
                                                 item['delegate'],item['login_money'],item['real_money'],item['status'],item['login_time'],item['Registration'],item['org_number'],
                                                 item['taxpayer_number'],item['credit_number'],item['company_type'],item['profession'],item['approved_date'],item['registration_org'],
                                                 item['region'],item['english_name'],item['old_name'],item['business_mode'],item['staff_size'],item['business_date'],item['business_scope'],
                                                item['partner_info'],item['main_member'],item['touzilist'],item['fenzhilist'],item['changelist']))
```
### 将items存入redis队列中
```
class RdisPipline(object):
    def __init__(self):
        #链接数据库
        self.r = redis.Redis(host='39.104.62.136', port=6379,db=0)
    def process_item(self, item, spider):
        loop = asyncio.get_event_loop()
        # 设置需要插入的行的名称
        import json
        @asyncio.coroutine
        def go():
            jieguo = json.dumps(dict(item))
            self.r.lpush('json', jieguo)
            self.r.lpush('shuliang', jieguo)
        loop.run_until_complete(go())
        print('成功倒入redis=============================================================================================')
```
## 使用布隆过滤器按位去重
```
class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, server, key, blockNum=1):
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31]
        # self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.server = server
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        ret = True

        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)
```

## 由于后来公司购买了企查查全部的公司名称和url，所以获取的方式也发生了变化，改为从接口获取1000个url，并返回id和内容。
### 使用接口获取url
```
    def start_requests(self):
        while True:
            try:
                appid = '********'
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
```
### 完善企查查信息页面的采集
```
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
```

## 最后使用flask提供一个api接口，当用户访问时可以自动更新页面信息。

```
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_api import app#这里要和run.py对应
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(****) #flask默认的端口
IOLoop.instance().start()
```
```
306 lines (300 sloc)  17.3 KB
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
```


