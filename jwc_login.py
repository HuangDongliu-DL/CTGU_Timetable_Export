#encoding=utf-8
import sys
import os
import time
import pickle
from io import BytesIO

import requests
from bs4 import BeautifulSoup
# 下面两行主要为解决在Rpi上运行报错的问题
import locale
locale.setlocale(locale.LC_ALL, 'C')
import tesserocr
from PIL import Image


class Login:
    '''
    用于登入教务处
    '''
    def __init__(self,username,password):
        # 用户账好
        self.username = username
        # 用户密码
        self.password = password
        # 获取验证码URL
        self.code_url = "http://210.42.38.26:84/jwc_glxt/ValidateCode.aspx"
        # 登入URL
        self.login_url = "http://210.42.38.26:84/jwc_glxt/Login.aspx"
        # 创建session对象
        self.session = requests.session()
        #如果登入成功该变量会被置为True
        self.login_status = False
    def __call__(self):
        '''
        开始登入
        '''
        # 如果有缓存文件就读取缓存文件若没有就直接登入
        if self.username in os.listdir('./cookies/'):
            # 读取缓存
            print("检测到缓存文件，开始读取缓存文件。。。。。")
            with open("./cookies/" + self.username, 'rb') as f:
                cookies = pickle.load(f)
                self.session.cookies.update(cookies)
            if self.is_login(self.session):
                print("读取缓存文件成功缓存cookie成功")
                return self.session
            else:
                print("缓存文件过期，正在重新登入")
                self.re_login()
            return self.session
        else:
            self.re_login()
            return self.session
    def re_login(self):
        '''
        :function
            重新登入
        :return:
        '''
        viewstate = None
        eventvalidation = None

        img_byte= self.session.get(self.code_url).content
        img = Image.open(BytesIO(img_byte))
        code = tesserocr.image_to_text(img)
        log_in_data = self.session.get(self.login_url).text

        for i in BeautifulSoup(log_in_data, 'html.parser').find_all('input'):
            if i['name'] == "__VIEWSTATE":
                viewstate = i['value']
            if i['name'] == "__EVENTVALIDATION":
                eventvalidation = i['value']
        DATA = {
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            'txtUserName': self.username,
            'btnLogin.x': '17',
            'btnLogin.y': '20',
            'txtPassword': self.password,
            'CheckCode': code
        }
        HEARDER = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Origin": "http://210.42.38.26:84",
            "Referer": "http://210.42.38.26:84/jwc_glxt/Login.aspx",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        # 发送登入数据包
        respond = self.session.post(self.login_url,
                                    headers=HEARDER,
                                    data=DATA,
                                    allow_redirects=False)
        #如果登入成功会自动重定向，标志码为302，返回True。如果没有登入成功则重新登入直到成功
        if respond.status_code == 200:
            # 检测登入失败的原因
            respond_text = BeautifulSoup(respond.text, 'lxml').find('span', id='lblMsg')
            if "验证码不对" in respond_text.string:
                print("验证码错误,将再次尝试。。。")
            else:
                print("账号或者密码错误，。。。")
                input("请按ENTRY键退出")
                sys.exit()
            time.sleep(0.5)
        else:
            print('登入成功！！')
            # 刷新cookie缓存
            with open("./cookies/"+self.username,'wb') as f:
                pickle.dump(self.session.cookies,f)
            # 刷新登入状态
            self.login_status = True
        # 直到登入为止
        while self.login_status == False:
            self.re_login()
    def is_login(self,session):
        '''
        用于测试是否完成登入
        :param
            session:requests session对象
        :return
            True、False
        '''
        # 用于测试的链接
        Test_URL = "http://210.42.38.26:84/jwc_glxt/Stu_Notice/Notice_Query.aspx"
        r = session.get(url=Test_URL)
        soup = BeautifulSoup(r.text, 'lxml')
        for i in soup.find_all('script'):
            if "你尚未登录系统！请先登录为合法用户！" in repr(i):
                return False
        return True
