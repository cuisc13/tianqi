#-*-coding:utf-8-*-

import json
from urllib2 import urlopen
import sys

identme_url = 'http://ident.me'
tianqi_url = 'https://www.baidu.com/home/other/data/weatherInfo'
'''
tianqi_res = urlopen(tianqi_url+'?ip=%s' % globalip).read()
tianqi_jso = json.loads(tianqi_res)

weather = tianqi_jso['data']['weather']
content = weather['content']
today = content['today']
city = content['city']

print (u"当前城市:%s" % city)

for k in today:
    print("%s:  %s" %(k,today[k]))
'''

def get_ip():
    globalip = urlopen(identme_url).read()
    print("当前IP：%s" % globalip)
    return globalip

def get_city():
    city = ''
    if len(sys.argv)>2:
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

def print_w(w):
    fmt = u'''
    {city}
    {0[time]}
    {0[condition]}
    {0[wind]}
    {0[temp]}
    '''
    content = w['data']['weather']['content']
    city = content['city']
    days = ['today','tomorrow','thirdday','fourthday', 'fifthday']
    for day in days:
        print(fmt.format(content[day],city=city))
    pass

def main():
    ip = get_ip()
    city = get_city()
    weather=get_weather(city=city,ip=ip)
    print_w(weather)
    pass

if __name__ == '__main__':
    main()
