#!/usr/bin/env python3
# *-- coding: utf-8 --*

import requests
import json


def forcast(args, nick, channel, c, e):
    args = args.split()
    if len(args) == 0:
        return "%s: 请输入城市" % nick
    if len(args) == 1:
        city = args[0].strip('市') + '市'
        location = _get_city_location(city)
    if len(args) == 2:
        city = args[0].strip('市') + '市'
        place = args[1]
        location = _get_city_location(city, place)
    if location is not False:
        darksky_key = "c0930b16e7d43d90e3770bf306c25260"
        darksky_url = "https://api.darksky.net/forecast/%s/%s?lang=zh&units=si" % (darksky_key, location)
        con1 = requests.get(darksky_url)
        # print(con1.content)
        js1 = json.loads(con1.content)
        return "%s: (%s) 即时天气 %s 实时温度 %.2f℃ 体感温度 %.2f℃ 降水概率 %d%% 湿度 %d%% 紫外线指数 %d 短时预报 %s 本周天气 %s" \
               % (nick, location, js1['currently']['summary'], js1['currently']['temperature'], js1['currently']['apparentTemperature'],
                  js1['currently']['precipProbability']*100, js1['currently']['humidity']*100, js1['currently']['uvIndex'], js1['hourly']['summary'], js1['daily']['summary'])
    else:
        return "%s: 城市输入有误" % nick


def _get_city_location(city, place=None):
    if place:
        baidu_url = "https://api.map.baidu.com/geocoder/v2/?output=json&address=%scity=%s&ak=%s&coordtype=wgs84ll" % \
                (city, place, "6ea5c34d2e11b0ef256a870433dc098d")
    else:
        baidu_url = "https://api.map.baidu.com/geocoder/v2/?output=json&address=%scity=%s&ak=%s&coordtype=wgs84ll" % \
                (city, city, "6ea5c34d2e11b0ef256a870433dc098d")
    con = requests.get(baidu_url)
    js = json.loads(con.content)
    if 'result' in js.keys() and 'location' in js['result'].keys():
        return "%.4f,%.4f" % (js['result']['location']['lat'], js['result']['location']['lng'])
    return False
