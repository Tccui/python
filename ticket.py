#!/usr/bin/python
# _*_ coding:utf-8 _*_

import requests
import argparse
import datetime
import re
import MySQLdb
from prettytable import PrettyTable
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

now = datetime.datetime.now()
tomorrow = now + datetime.timedelta(days=1)
tomorrow = tomorrow.strftime('%Y-%m-%d')

argument = argparse.ArgumentParser()
argument.add_argument('--fromcity', '-f', default='beijing')
argument.add_argument('--tocity', '-t', default='shanghai')
argument.add_argument('--date', '-d', default=tomorrow)

args = argument.parse_args()

from_station = args.fromcity
to_station = args.tocity
Date = args.date

'''
# 直接从js中获取地点的代码,只能按拼音查
stationlist_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
r = requests.get(stationlist_url, verify=False)
stationlist = r.content
ToStation = ''
FromStation = ''

placea = stationlist.find(from_station)
placeb = stationlist.find(to_station)

for i in range(-4, -1):
    FromStation += stationlist[placea + i]
for i in range(-4, -1):
    ToStation += stationlist[placeb + i]
'''
# 查询地点代码，从数据库中查，输入简写，中文，拼音都可以
db = MySQLdb.connect("120.77.144.110", "root", "Mysql123456", "test")
cursor = db.cursor()
# 设置编码
cursor.execute("set names utf8")
# 起始车站查询
sql = "select code from city where name like '%s' or shorthand like '%s' or phoneticize like '%s' "\
      % (from_station, from_station, from_station)
cursor.execute(sql)
result = cursor.fetchone()
if len(result) <= 0:
    print("未找到起始车站")
    exit()
else:
    FromStation = result[0]
# 终点站查询
sql = "select code from city where name like '%s' or shorthand like '%s' or phoneticize like '%s' "\
      % (to_station, to_station, to_station)
cursor.execute(sql)
result = cursor.fetchone()
if len(result) <= 0:
    print("未找到终点车站")
    exit()
else:
    ToStation = result[0]

query_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=' + Date + '&leftTicketDTO.from_station=' + FromStation +'&leftTicketDTO.to_station=' + ToStation + '&purpose_codes=ADULT'

r = requests.get(query_url, verify=False)
'''
# 将结果写入文件
with open('json.txt', 'w') as fp:
    fp.write(str(r.json()))
'''
try:
    if 'result' in r.json()["data"]:
        result = r.json()["data"]["result"]
        pt = PrettyTable()

        header = '车次 车站 到站时间 时长 一等座 二等座 软卧 硬卧 硬座 无座'.split()
        pt._set_field_names(header)
        for item in result:
            ptrow = []
            data_list = item.split('|')
            ptrow.append(data_list[3])
            sql = "select name from city where code='%s'" % (data_list[6])
            cursor.execute(sql)
            formStation = cursor.fetchone()
            sql = "select name from city where code='%s'" % (data_list[7])
            cursor.execute(sql)
            toStation = cursor.fetchone()
            ptrow.append('\n'.join([formStation[0], toStation[0]]))
            ptrow.append('\n'.join([data_list[8], data_list[9]]))
            ptrow.append(data_list[10])
            ptrow.append(data_list[31] or '--')
            ptrow.append(data_list[30] or '--')
            ptrow.append(data_list[23] or '--')
            ptrow.append(data_list[28] or '--')
            ptrow.append(data_list[29] or '--')
            ptrow.append(data_list[26] or '--')
            pt.add_row(ptrow)
        print pt
    else:
        print '这两个站点没有直达列车'
except:
    print '查询异常'
# 关闭数据库连接
db.close()
