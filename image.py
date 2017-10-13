#! /usr/bin/env python
# _*_ coding:utf-8 _*_
# 多线程爬取糗事百科成人网图片

import requests
import MySQLdb
import threading
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class getImg:
    def __init__(self):
        # 糗事百科链接
        self.url = "http://www.qiubaichengren.com/%s.html"
        # 每一次爬取的页数
        self.page_num = 10
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.header = {'User-Agent': self.user_agent}

    # 开始多线程爬取
    def start(self):
        for i in range(1, self.page_num + 1):
            try:
                thred = threading.Thread(target=self.load_html, args=(str(i), ))
                thred.start()
            except:
                print('多线程异常')
                exit()
    # 爬取网页内容
    def load_html(self, page):
        try:
            url = self.url % page
            data = requests.get(url, verify=False)
            data.encoding = 'gb2312'
            soup = BeautifulSoup(data.text, 'lxml')
            info = soup.find_all("img")
            sql = 'insert into image (title, url) values'
            for item in info:
                attrs = item.attrs
                if attrs.has_key('alt') and attrs.has_key('src'):
                    sql += "('%s', '%s')," % (attrs['alt'].encode('utf-8'), attrs['src'].encode('utf-8'))
            sql = sql[0:-1]
            self.add_data(sql)
        except:
            print('获取网页数据异常')
    def add_data(self, sql):
        try:
            db = MySQLdb.connect('120.77.144.110', 'root', '123456', 'qiushibaike')
            cursor = db.cursor()
            cursor.execute("set names utf8")
            cursor.execute(sql)
            db.commit()
            db.close()
        except:
            print('数据库错误')
img = getImg()
img.start()
