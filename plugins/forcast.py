#!/usr/bin/env python3
# *-- coding: utf-8 --*

import requests
import json


def forcast(args, nick, channel, c, e):
    args = args.split()
    if len(args) == 0:
        return "%s: 请输入城市" % nick
    city = args[0].strip('市') + '市'
    location = _get_city_location(city)
    if location is not False:
        darksky_key = "c0930b16e7d43d90e3770bf306c25260"
        darksky_url = "https://api.darksky.net/forecast/%s/%s?lang=zh&units=si" % (darksky_key, location)
        con1 = requests.get(darksky_url)
        # print(con1.content)
        js1 = json.loads(con1.content)
        return "%s: 即时天气 %s 实时温度 %.2f℃ 体感温度 %.2f℃ 降水概率 %d%% 湿度 %d %% " \
               % (nick, js1['currently']['summary'], js1['currently']['temperature'], js1['currently']['apparentTemperature'],
                  js1['currently']['precipProbability']*100, js1['currently']['humidity']*100)
    else:
        return "%s: 城市输入有误" % nick


def _get_city_location(city):
    baidu_url = "https://api.map.baidu.com/geocoder/v2/?output=json&address=%scity=%s&ak=%s" % \
                (city, city, "6ea5c34d2e11b0ef256a870433dc098d")
    con = requests.get(baidu_url)
    js = json.loads(con.content)
    if 'result' in js.keys() and 'location' in js['result'].keys():
        return "%.4f,%.4f" % (js['result']['location']['lat'], js['result']['location']['lng'])
    return False
