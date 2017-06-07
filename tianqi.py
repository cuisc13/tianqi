#!env python2.7
#-*-coding:utf-8-*-
#autho:Tony Cui
#email:cuisc13@gmail.com

import json
from urllib2 import urlopen
import sys
import sqlite3
import os

identme_url = 'http://ident.me'
netcn_url = 'http://www.net.cn/static/customercare/yourip.asp'
tianqi_url = 'https://www.baidu.com/home/other/data/weatherInfo'
city_url = 'http://ip.taobao.com/service/getIpInfo.php' # 淘宝的这个api有频率限制  小气

# city_url = 'http://whois.pconline.com.cn/ipJson.jsp'
home = os.environ['HOME'] # 获得家目录
city_db = home +'/.config/tianqi/city.db'

def get_ip():
    # identme 是境外站点 速度慢
    #globalip = urlopen(identme_url).read()
    html = urlopen(netcn_url).read()

    # net.cn 是国内站点速度快
    ip = html[html.find('<h2>')+4:html.find('</h2>')].split(', ')[0]
    iptmp = ip.split('.')
    iptmp[1], iptmp[2] = '**','**'
    ip_fake = '.'.join(iptmp)
    print("当前IP：%s" % ip_fake)
    return ip

def print_localcity(ip):
    '''
    js = urlopen(city_url + "?ip=%s" % ip).read()
    jso = json.loads(js)
    fmt = u'当前位置: {0[area]}({0[area_id]}), {0[region]}({0[region_id]}), {0[city]}({0[city_id]})'
    print(fmt.format(jso['data']))
    '''
    url = city_url + "?ip=%s" % ip
    d = urlopen(url).read()
    jso = json.loads(d[d.find('({')+1:d.find('})')+1].decode('gbk'))
    fmt = u'当前位置: {0[pro]}({0[proCode]}), {0[city]}({0[cityCode]})'
    print(fmt.format(jso))


def print_termicity(city):
    conn = sqlite3.connect(city_db)
    cur = conn.cursor()

    sql = '''
    select
    city.name,city.code,country.name,country.code,city.province_id
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

    city = {}
    n = len(citys)
    if n > 1:
        city['name'] = citys[0][0]
        city['code'] = citys[0][1]
    elif n == 1:
        city['name'] = citys[0][2]
        city['code'] = citys[0][3]
        city['city_name'] = citys[0][0]
        city['city_code'] = citys[0][1]
    else:
        return

    sql = 'select name,code from province where id=%d'%citys[0][-1]
    cur.execute(sql)
    province = cur.fetchall()[0]
    city['province'] = province[0]
    city['province_code'] = province[1]
    cur.close()
    conn.close()
    s = ""
    if n > 1:
        s=u"查询城市:{0[province]}({0[province_code]}),{0[name]}({0[code]})".format(city)
    elif n == 1:
        s=u"查询城市:{0[province]}({0[province_code]}),{0[city_name]}({0[city_code]}), {0[name]}({0[code]})".format(city)

    print(s)

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
    print("")
    fmt = u'''{today}\t{0[time]}
日期\t{0[date]}
天气\t{0[condition]}
风力\t{0[wind]}
温度\t{0[temp]}
'''
    pm25_fmt = u'''PM2.5\t{0[pm25]}
污染\t{0[pollution]}
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
        line = ""
        pm25_line = ""
        weather_line = ""
        today = daym[day].decode('utf8')
        if day == 'today':
            content[day]['time'] += u"\n农历\t"+content['calendar']['lunar']
            pm25_line = pm25_fmt.format(content[day])
        weather_line = fmt.format(content[day],today=today, city=city)
        line = weather_line + pm25_line
        print(line)
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
