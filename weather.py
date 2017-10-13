#!/usr/bin/python
# _*_ coding:utf-8 _*_
# 引入请求包
import requests
# 引入参数处理包
import argparse
# 引入日期包
import datetime
# 引入表格式处理包
from prettytable import PrettyTable
# 引入https处理包
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 引入数据库处理
import MySQLdb
# 禁用安全警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 天气图标
weatherInfo = {
    'icoUrl': 'http://mat1.gtimg.com/weather/2014gaiban/',
    'data': {
        '00': {'bg': 'qing',        'ico': 'qing',           'name': '晴'},
        '01': {'bg': 'duoyun',      'ico': 'duoyun',         'name': '多云'},
        '02': {'bg': 'yin',         'ico': 'yin',            'name': '阴'},
        '03': {'bg': 'xiaoyu',      'ico': 'zhenyu',         'name': '阵雨'},
        '04': {'bg': 'leizhenyu',   'ico': 'leizhenyu',      'name': '雷阵雨'},
        '05': {'bg': 'leizhenyu',   'ico': 'leizhenyu',      'name': '雷阵雨并伴有冰雹'},
        '06': {'bg': 'xiaoyu',      'ico': 'yujiaxue',       'name': '雨夹雪'},
        '07': {'bg': 'xiaoyu',      'ico': 'xiaoyuzhongyu',  'name': '小雨'},
        '08': {'bg': 'xiaoyu',      'ico': 'xiaoyuzhongyu',  'name': '中雨'},
        '09': {'bg': 'dayubaoyu',   'ico': 'dayubaoyu',      'name': '大雨'},
        '10': {'bg': 'dayubaoyu',   'ico': 'dayubaoyu',      'name': '暴雨'},
        '11': {'bg': 'dayubaoyu',   'ico': 'dayubaoyu',      'name': '大暴雨'},
        '12': {'bg': 'dayubaoyu',   'ico': 'dayubaoyu',      'name': '特大暴雨'},
        '13': {'bg': 'xue',         'ico': 'zhenxue',        'name': '阵雪'},
        '14': {'bg': 'xue',         'ico': 'xiaoxuezhongxue','name': '小雪'},
        '15': {'bg': 'xue',         'ico': 'xiaoxuezhongxue','name': '中雪'},
        '16': {'bg': 'xue',         'ico': 'daxuebaoxue',    'name': '大雪'},
        '17': {'bg': 'xue',         'ico': 'daxuebaoxue',    'name': '暴雪'},
        '18': {'bg': 'wu',          'ico': 'wu',             'name': '雾'},
        '19': {'bg': 'xiaoyu',      'ico': 'dongyu',         'name': '冻雨'},
        '20': {'bg': 'shachenbao',  'ico': 'shachenbao',     'name': '沙尘暴'},
        '21': {'bg': 'xiaoyu',      'ico': 'xiaoyuzhongyu',  'name': '小雨-中雨'},
        '22': {'bg': 'dayubaoyu',   'ico': 'dayubaoyu',      'name': '中雨-大雨'},
        '23': {'bg': 'dayubaoyu',   'ico': 'dayubaoyu',      'name': '大雨-暴雨'},
        '24': {'bg': 'dayubaoyu',   'ico': 'dayubaoyu',      'name': '暴雨-大暴雨'},
        '25': {'bg': 'dayubaoyu',   'ico': 'dayubaoyu',      'name': '大暴雨-特大暴雨'},
        '26': {'bg': 'xue',         'ico': 'xiaoxuezhongxue','name': '小雪-中雪'},
        '27': {'bg': 'xue',         'ico': 'daxuebaoxue',    'name': '中雪-大雪'},
        '28': {'bg': 'xue',         'ico': 'daxuebaoxue',    'name': '大雪-暴雪'},
        '29': {'bg': 'fuchen',      'ico': 'mai',            'name': '浮尘'},
        '30': {'bg': 'fuchen',      'ico': 'mai',            'name': '扬沙'},
        '31': {'bg': 'shachenbao',  'ico': 'shachenbao',     'name': '强沙尘暴'},
        '53': {'bg': 'mai',         'ico': 'mai',            'name': '霾'}
    }
}
# 空气质量
weatherQuality = {
    'data': {
        "优": {"level": "一级", "affect": "无", "lovetips": "各类人群可正常活动"},
        "良": {"level": "二级", "affect": "某些污染物可能对极少数异常敏感人群健康有较弱影响",   "lovetips": "建议极少数异常敏感人群减少户外活动"},
        "轻度污染": {"level": "三级", "affect": "易感人群症状有轻度加剧，健康人群出现刺激症状",   "lovetips": "建议老幼和心脏病、呼吸系统疾病患者减少长时间、高强度的户外锻炼"},
        "中度污染": {"level": "四级", "affect": "加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响",   "lovetips": "建议疾病患者避免长时间、高强度的户外锻练，一般人群适量减少户外运动。"},
        "重度污染": {"level": "五级", "affect": "心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状",   "lovetips": "建议老幼和心脏病、肺病患者停留在室内停止户外运动，一般人群减少户外运动"},
        "严重污染": {"level": "六级", "affect": "健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病",   "lovetips": "建议老幼和病人留在室内，避免体力消耗，一般人群应避免户外活动"}
    }
}
# 风向风速
windDir = ['', '东北风', '东风', '东南风', '南风', '西南风', '西风', '西北风', '北风', '旋转不定']
windPower = ['微风', '3-4级', '4-5级', '5-6级', '6-7级', '7-8级', '8-9级', '9-10级', '10-11级', '11-12级']

weekDay = ['一', '二', '三', '四', '五', '六', '日']
argument = argparse.ArgumentParser()
argument.add_argument('--city', '-c', default='深圳')
argument.add_argument('--week', '-w', action='store_true')
args = argument.parse_args()
city = args.city
week = args.week
db = MySQLdb.connect('120.77.144.110', 'root', 'Mysql123456', 'weather')
cursor = db.cursor()
cursor.execute("set names utf8")
sql = " select code from area where spell = '%s' or title = '%s'" % (city, city)
cursor.execute(sql)
result = cursor.fetchone()
db.close()
if len(result) <= 0:
    print('暂无')
    exit()
code = result[0]
url = "http://weather.gtimg.cn/city/%s.js" % code
data = requests.get(url, verify=False)
# data示例见weather.json
data = eval(data.text.split('=')[1][0:-1])
# 空气质量数据，没有具体用到
url = "http://weather.gtimg.cn/aqi/%s.json" % code
quality_data = requests.get(url, verify=False)
quality_data = quality_data.text[5:-1]

header = "时间 天气 温度 风向 风速 天气图标".split()
pt = PrettyTable()
pt._set_field_names(header)
i = 1
now = datetime.datetime.now()
for item in data['wk']['0']:
    ptrow = []
    if i % 2 == 0:
        tp = item['tmin']
        img_url = weatherInfo['icoUrl'] + 'TB_' + weatherInfo['data'][item['wt']]['ico'] + '_yejian_min.png'
        if i == 2:
            time = '今天夜间'
        elif i == 4:
            time = '明天夜间'
        else:
            days = i / 2 - 1
            delta = datetime.timedelta(days=days)
            time = now + delta
            time = '周' + weekDay[time.weekday()] + '夜间'
    else:
        tp = item['tmax']
        img_url = weatherInfo['icoUrl'] + 'TB_' + weatherInfo['data'][item['wt']]['ico'] + '_baitian_min.png'
        if i == 1:
            time = '今天白天'
        elif i == 3:
            time = '明天白天'
        else:
            days = (i + 1) / 2 - 1
            delta = datetime.timedelta(days=days)
            time = now + delta
            time = '周' + weekDay[time.weekday()] + '白天'
    ptrow.append(time)
    ptrow.append(weatherInfo['data'][item['wt']]['name'])
    ptrow.append(tp)
    ptrow.append(windDir[int(item['wd'])] or '无风')
    if windDir[int(item['wd'])].strip() == '':
        ptrow.append('无风')
    else:
        ptrow.append(windPower[int(item['wp'])])
    ptrow.append(img_url)
    pt.add_row(ptrow)
    # 默认只返回两天的天气情况
    if i == 4 and week == False:
        break
    i = i + 1
print pt



