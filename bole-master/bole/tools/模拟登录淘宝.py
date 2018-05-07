#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'JustFantasy'

import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import re
import requests

# 模拟登录淘宝类
# 登录淘宝流程
# 1、请求地址https://login.taobao.com/member/login.jhtml获取到token
# 2、请求地址https://passport.alibaba.com/mini_apply_st.js?site=0&token=1L1nkdyfEDIA44Hw1FSDcnA&callback=callback 通过token换取st
# 3、请求地址https://login.taobao.com/member/vst.htm?st={st}实现登录
class Taobao:

    # 初始化方法
    def __init__(self):
        # 登录的URL，获取token
        self.request_url = 'https://login.taobao.com/member/login.jhtml'
        # 通过st实现登录的URL
        self.st_url = 'https://login.taobao.com/member/vst.htm?st={st}'
        # 用户中心地址
        self.user_url = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a1z02.1.a2109.d1000368.19bc782dVxGtP4&nekot=1470211439694'
        # 代理IP地址，防止自己的IP被封禁
        # self.proxy_ip = 'http://120.193.146.97:843'
        # 登录POST数据时发送的头部信息
        self.request_headers =  {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept - Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accept - Encoding': "gzip, deflate, br",
            # 'Cookie':"t=dbcf36ce29917be27cdc21a6c44388c0; isg=BK-vctIOKZLc9i18E4wOS9VYPcN5_ALTjCq8KcE8S54lEM8SySSTxq3CloAuc9vu; cna=E87pEdwxl20CAXO++RLZ+Xup; um=2BA477700510A7DF4BFD5F1C07D83177D2BBD7BF48D915C59EE2481B340B7489946C798DF97C02A3CD43AD3E795C914C28EAC278DA620030A52CA20815F3CC03; mt=np=&ci=0_0; _cc_=W5iHLLyFfA%3D%3D; tg=0; thw=cn; _m_user_unitinfo_=unit|unsz; _m_unitapi_v_=1508566261407; _m_h5_tk=fb46a4976f536f32ab9acfef3710f337_1521767059050; _m_h5_tk_enc=a90d76378def91a7514173a994fff466; cookie2=13c72ab34cd2f79023ebf39da989a61e; _tb_token_=bb3f30f5a3fe; _mw_us_time_=1521764287318; v=0; uc1=cookie14=UoTeP78XqucSaQ%3D%3D&lng=zh_CN&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&existShop=false&cookie21=W5iHLLyFeYZ1WM9hVnmS&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0; uc3=nk2=o%2FM%2F2V08WfqQ6Q%3D%3D&id2=Uoe8jJBG40sq8w%3D%3D&vt3=F8dBz4KAq1fL%2FdwF0m8%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTUyMTc2NjcwMA%3D%3D; lgc=%5Cu674E%5Cu5143%5Cu660A9286; tracknick=%5Cu674E%5Cu5143%5Cu660A9286; dnk=%E6%9D%8E%E5%85%83%E6%98%8A9286; sg=654; csg=7030da6f; cookie1=VFCt7a%2FkeF%2Bxv2p%2BQfDT6yMT9FV3fLLsbirc29QX3K4%3D; unb=1686316895; skt=32b2f81fedabb0c5; _l_g_=Ug%3D%3D; _nk_=%5Cu674E%5Cu5143%5Cu660A9286; cookie17=Uoe8jJBG40sq8w%3D%3D",
            'Host':'login.taobao.com',
            'Upgrade - Insecure - Requests': "1",
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Referer' : '"https://login.taobao.com/member/login.jhtml"',
            'Connection' : 'Keep-Alive'
        }
        # 用户名
        self.username = '15736722502'
        # ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua= "106#+YoBBbBEBIEBGQKaBBBBBpZb5uHZS0GR9Pbft0GcGPzVkCCN9VbVy0dhkfYuy0tQ94dYo0+hk4IZk0Z1kUUZoCtN9VUu0JkKBBgbylZy8BP7A8SKBB8byltqmWt/BCBEylmi4gO0ylmbyl6v3pDbgImbyxzz0q4wylmUPgO0yqebyl633pVYw2LKBKhvOu5h6meaNMuVWV9SncNCyGzX9UyjcJXbsYTs7JyKBmxbT1bvmfqBUbT+uVpg5LtFwyMM6h0EUy91Z1JY9h04wyQcYXL29lMGUsaZlQQEecx+wztYXN9lcmawSboBKImU1Zzz0CLKBBCxcRxBlCoBKBBB7NzIBCBoBBKItFoKBKZRylDvmVtpKBl4OV1n+SungBNanFoKBB7bylDvmVAOBCBAymmi4Pm5ECoBp4kb1ZJbhbDoByvpqsSNRtMkX8EIECoBp4lb1ZJD3bDoByvpqsSNRtMkX8EIECoBp4kb1ZJD+9n4YohVtioOYBi2m5Y1NCoBAVlb1ZzzBBEpKB3a7TLNRkung+pKXf02Rkb1BCBoBBKM7xLKBKTRylDv3Bk2KCCmaNJ5+SRGUzUZCCLTfkRklCoBKBBB7NF5BCB5tcmi4gQXpQDoBFxMWf7kRtMkLDo++DgkRmsKBBCBBAJMNCoBAVlb1ZzzmVLpKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gQGnBDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv3BwKKCCmaNJ5+SRGUzUZCCLTfkRkNCoBAVlb1ZzzmPEpKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gQ+QCDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv3BO1KCCmaNJ5+SRGUzUZCCLTfkRkNCoBAVlb1ZzzX+opKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gQnqbDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv3BxhKCCmaNJ5+SRGUzUZCCLTfkRkNCoBAVlb1ZzzXatpKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gQiPCDoBFxMWf7kRtMkLDo++DgkR6yKBBebklDvGCoBpukYIZwD0qX6v96aeDsufsEGY2pcemR2GCoBpukYSYwP0qX6Q96aeDsufsEGY2pcemR2GCoBpukYSYw70qm6126aeDsufsEGY2pcemR2GCoBpukYSYwC0qm6qz6aeDsufsEGY2pcemR2GCoBpukYSYwW0qm6jz6aeDsufsEGY2pcemR23CoBAPkYSYwV0qmbyBM54P26Yoh2fJYa8Up2mDr2lCoBKBBB7Nz="        # 密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '965f5ef1a2fa17f50b1ec1e4b68d1560999b47a94ecaa94af40f639cacfb2301dcca37f6e5ce030e4595fb4ca441046a71024f4b9c3db1efd5eff0f00fd3fff48f2f94e59a546a3219c250cf05a4c2515262e109c76e154e33fb3cdb9bc2777f811812212c7606bfd2ed621458bd469433da6f884d06060e7d10e105c3fcce51'
        self.post = {
            'ua': self.ua,
            'TPL_password': "",
            'TPL_checkcode': '',
            'ncoSig': "",
            'ncoSessionid': "",
            'ncoToken':"c1a2ac43a023dcd02e584173e47218fc51bc43fc",
            'slideCodeShow':"false",
            'useMobile':"false",
            'lang':"zh_CN",
            'loginsite':"0",
            'newlogin':"0",
            'TPL_redirect_url':"",
            'from':"tb",
            'fc':"default",
            'style':"default",
            'css_style':"",
            'keyLogin':"false",
            'qrLogin':"true",
            'newMini':"false",
            'newMini2':"false",
            'tid':"",
            'loginType':"3",
            'minititle':"",
            'minipara':"",
            'pstrong':"",
            'sign':"",
            'need_sign':"",
            'isIgnore':"",
            'full_redirect':"",
            'sub_jump':"",
            'popid':"",
            'callback':"",
            'guf':"",
            'not_duplite_str':"",
            'need_user_id':"",
            'poy':"",
            'gvfdcname':"10",
            'gvfdcre':"",
            'from_encoding':"",
            'sub':"",
            'loginASR':"1",
            'loginASRSuc':"1",
            'allp':"",
            'oslanguage':"zh-CN",
            'sr':"1920*1080",
            'osVer':"",
            'naviVer':"firefox|52",
            'osACN':"Mozilla",
            'osAV':"5.0+(Windows)",
            'osPF':"Win32",
            'miserHardInfo':"",
            'appkey':"00000000",
            'nickLoginLink':"",
            'mobileLoginLink':"https://login.taobao.com/member/login.jhtml?useMobile=true",
            'showAssistantLink':"",
            'um_token':"HV01PAAZ0b8bd9e5d3a1a09c5ab45110006a53c8",
            'TPL_username': self.username,
            'TPL_password_2': self.password2,
        }
        # 将POST的数据进行编码转换
        # self.post_data = urllib.parse.urlencode(self.post).encode(encoding='GBK')
        # 设置代理
        # self.proxy = urllib.request.ProxyHandler({'http': self.proxy_ip})
        # 设置cookie
        self.cookie = http.cookiejar.LWPCookieJar()
        # 设置cookie处理器
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        # 设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib.request.build_opener(self.cookieHandler, urllib.request.HTTPHandler)
        # 赋值J_HToken
        self.J_HToken = ''
        # 登录成功时，需要的Cookie
        self.newCookie = http.cookiejar.CookieJar()
        # 登陆成功时，需要的一个新的opener
        self.newOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.newCookie))

    # 利用st码进行登录
    # 这一步我是参考的崔庆才的个人博客的教程，因为抓包的时候并没有抓取到这个url
    # 但是如果不走这一步，登录又无法成功
    # 区别是并不需要传递user_name字段，只需要st就可以了

    # 程序运行主干
    def main(self):
        try:
            # 请求登录地址， 此时返回的页面中有两个js的引入
            # 位置是页面的前两个JS的引入，其中都带有token参数
            session = requests.Session()
            response=session.post(self.request_url, self.post, self.request_headers)
            content = response.content.decode('gbk')

            # 抓取页面中的两个获取st的js
            pattern = re.compile('<script src=\"(.*)\"><\/script>')
            match = pattern.findall(content)

            # [
            # 'https://passport.alibaba.com/mini_apply_st.js?site=0&token=1f2f3ePAx5b-G8YbNIlDCFQ&callback=callback',
            # 'https://passport.alipay.com/mini_apply_st.js?site=0&token=1tbpdXJo6W1E4bgPCfOEiGw&callback=callback',
            # 'https://g.alicdn.com/kissy/k/1.4.2/seed-min.js',
            # 'https://g.alicdn.com/vip/login/0.5.43/js/login/miser-reg.js?t=20160617'
            # ]
            # 其中第一个是我们需要请求的JS，它会返回我们需要的st
            # print(match)


            # 如果匹配到了则去获取st
            if match:
                # 此时可以看到有两个st， 一个alibaba的，一个alipay的，我们用alibaba的去实现登录
                request = urllib.request.Request(match[0])
                response =session.get(match[0])
                content = response.content.decode('gbk')

                # {"code":200,"data":{"st":"1lmuSWeWh1zGQn-t7cfAwvw"} 这段JS正常的话会包含这一段，我们需要的就是st
                print(content)

                # 正则匹配st
                pattern = re.compile('{"st":"(.*?)"}')
                match = pattern.findall(content)
                # 利用st进行登录
                if match:
                    st_url = self.st_url.format(st=match[0])
                    response = session.get(st_url, headers=self.request_headers)
                    content = response.content.decode('gbk')
                    # print(content)

                    # 检测结果，看是否登录成功
                    pattern = re.compile('top.location.href = "(.*?)"', re.S)
                    match = re.findall(pattern, content)
                    print(match)
                    if match:
                        print(u'登录网址成功')
                    else:
                        print(u'登录失败')
            else:
                print(u'无法获取到st，请检查')
                return

            # 请求用户中心，查看打印出来的内容，可以看到用户中心的相关信息
            response = session.get(self.user_url)
            page = response.content.decode('gbk')
            pattern1 = re.compile("JSON\.parse(.*?)</script>",re.S)
            info = re.findall(pattern1,page)
            print(info)

        except urllib.error.HTTPError as e:
            print(u'请求失败，错误信息：', e.msg)



taobao = Taobao()
taobao.main()
