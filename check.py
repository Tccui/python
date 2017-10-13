#!/usr/bin/python
# _*_ coding:utf-8 _*_
# 检查12306地名编码对否有变
# 引入请求包
import requests
# 引入参数处理包
import argparse
# 引入日期包
import datetime
# 引入正则包
import re
# 引入数据库处理
import MySQLdb
# 引入表格式处理包
from prettytable import PrettyTable
# 引入https处理包
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 连接数据库
db = MySQLdb.connect("120.77.144.110", "root", "Mysql123456", "test")
cursor = db.cursor()
cursor.execute("set names utf8")
# 城市js文件
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
r = requests.get(url, verify=False)
station_list = r.content
list_arr = station_list.split('@')
# 删除第一个元素
del list_arr[0]
for city in list_arr:
    city_arr = city.split('|')
    sql = "select * from city where code = '" + city_arr[2] + "'"
    cursor.execute(sql)
    results = cursor.fetchone()
    n = len(results)
    if n == 0:
        sql = "insert into city (name, shorthand, code, phoneticize) values('" + city_arr[1] + "','" + city_arr[0] \
              + "','" + city_arr[2] + "','" + city_arr[3] + "')"
        cursor.execute(sql)
    else:
        if city_arr[0] != results[1] or city_arr[1] != results[2] or city_arr[3] != results[4]:
            sql = " update city set name = '" + city_arr[1] + "',shorthand='" + city_arr[0] + "',phoneticize='" \
                  + city_arr[3] + "' where code='" + results[3] + "'"
            cursor.execute(sql)
db.commit()
db.close()
print('ok')

