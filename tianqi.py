#!env python2
#-*-coding:utf-8-*-
#autho:Tony Cui
#email:cuisc13@gmail.com

import json
from urllib2 import urlopen
import sys
import sqlite3

identme_url = 'http://ident.me'
netcn_url = 'http://www.net.cn/static/customercare/yourip.asp'
tianqi_url = 'https://www.baidu.com/home/other/data/weatherInfo'
city_url = 'http://ip.taobao.com/service/getIpInfo.php'

def get_ip():
    # identme 是境外站点 速度慢
    #globalip = urlopen(identme_url).read()
    html = urlopen(netcn_url).read()

    # net.cn 是国内站点速度快
    ip = html[html.find('<h2>')+4:html.find('</h2>')].split(', ')[0]
    print("当前IP：%s" % ip)
    return ip

def print_localcity(ip):
    js = urlopen(city_url + "?ip=%s" % ip).read()
    jso = json.loads(js)
    fmt = u'''当前位置: {0[area]}({0[area_id]}), {0[region]}({0[region_id]}), {0[city]}({0[city_id]})
    '''
    print(fmt.format(jso['data']))

def print_termicity(city):
    conn = sqlite3.connect('./city.db')
    cur = conn.cursor()

    sql = '''
    select
    city.name,city.code,country.name,country.code
    from
    city
    inner join
    country
    on
    city.id = country.city_id
    where
    city.name like "%{city}%"
    or
    country.name like "%{city}%"
    limit 2
    ;
'''
    cur.execute(sql.format(city=city))
    citys = cur.fetchall()
    cur.close()
    conn.close()

    city = {}
    if len(citys) > 1:
        city['name'] = citys[0][0]
        city['code'] = citys[0][1]
    else:
        city['name'] = citys[0][2]
        city['code'] = citys[0][3]


    print(u"查询的城市: {0[name]}, 编号:{0[code]}".format(city))


def get_city():
    city = ''
    if len(sys.argv)>1:
        city = sys.argv[1]

    return city


def get_weather(city=None, ip=None):
    param = ""
    if city == "":
        param = "?ip=%s" % ip
    else:
        param = "?city=%s" % city
    res = urlopen(tianqi_url+param)
    jso = json.loads(res.read())
    return jso

def print_w(w,city=''):
    fmt = u'''{today}\t{0[time]}
日期\t{0[date]}
天气\t{0[condition]}
风力\t{0[wind]}
温度\t{0[temp]}
    '''
    content = w['data']['weather'].get('content')
    if not content:
        print(u"查询的城市不在服务范围内:%s"%city.decode('utf8'))
        return
    city = content['city']
    dayl = ['today','tomorrow','thirdday','fourthday', 'fifthday']
    daym = {'today':'今天','tomorrow':'明天','thirdday':'后天','fourthday':'第四天', 'fifthday':'第五天'}
    print(u"查询的城市: %s" % city)
    for day in dayl:
        print(fmt.format(content[day],today=daym[day].decode('utf8'), city=city))
    pass

def main():
    ip = get_ip()
    city = get_city()
    print_localcity(ip)
    if city:print_termicity(city)
    weather=get_weather(city=city,ip=ip)
    print_w(weather,city=city)
    pass

if __name__ == '__main__':
    main()
