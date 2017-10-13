#!/usr/bin/python
# _*_ coding:utf-8 _*_
# 引入请求包
import requests
# 引入参数处理包
import argparse
# 引入https处理包
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 引入爬虫包
from bs4 import BeautifulSoup
from urllib import urlencode
import time
# 引入redis包
import redis
from prettytable import PrettyTable
# 禁用安全警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
argument = argparse.ArgumentParser()
argument.add_argument('--city', '-c', default='深圳')

args = argument.parse_args()
city = args.city

redis = redis.Redis(host='127.0.0.1', port=6379, password='app123456', db=0)
city_code = redis.get(city)
if not city_code:
    params = urlencode({'cityname': city})
    time = int(time.time())
    url = "http://toy1.weather.com.cn/search?%s&callback=success_jsonpCallback&_=%s" % (params, time)
    data = requests.get(url, verify=False)
    # 默认选中第一个
    data = eval(data.text[22:-1])[0]
    city_code = data['ref'].split('~')[0]
    redis.set(city, city_code)
url = "http://www.weather.com.cn/weather/%s.shtml" % city_code
data = requests.get(url, verify=False)
'''
with open('test.php', 'w') as fp:
    fp.write(str(data.content))
'''
data.encoding = 'utf-8'
soup = BeautifulSoup(data.text, 'lxml')
# 日期
info = soup.select(".t.clearfix > li > h1")
date = []
for item in info:
    date.append(item.text)
# 天气状况
detail = []
info = soup.select(".t.clearfix > li > .wea")
for item in info:
    detail.append(item.text)
# 温度
tp = []
info = soup.select(".t.clearfix > li > .tem ")
for item in info:
    tp.append(item.text.replace("\n", ''))
# 风向
wind = []
info = soup.select(".t.clearfix > li > .win > em > span ")
for item in info:
    wind.append(item.attrs['title'])
# 风速
wp = []
info = soup.select(".t.clearfix > li > .win > i")
for item in info:
    wp.append(item.text)
header = '日期 天气 温度 风向 风速'.split()
pt = PrettyTable()
pt._set_field_names(header)
for i in range(1, 8):
    ptrow = []
    ptrow.append(date[i-1])
    ptrow.append(detail[i-1])
    ptrow.append(tp[i-1])
    n = (i-1) * 2
    wd = wind[n]+'->'+wind[n+1]
    ptrow.append(wd)
    ptrow.append(wp[i-1])
    pt.add_row(ptrow)
print(pt)
exit()


