#!/usr/bin/env python3
# *-- coding: utf-8 --*

import requests
import json


def forcast(args, nick, channel, c, e):
    args = args.split()
    if len(args) == 0:
        return "%s: 请输入城市" % nick
    city = args[0]
    amap_key = '3aa0d7cd316642f5484ecd4aa6886c91'
    amap_url = "http://restapi.amap.com/v3/geocode/geo?key=%s&address=%s&city=%s" % (amap_key, city, city)
    con = requests.get(amap_url)
    js = json.loads(con.content)
    con.close()
    if js['status'] == '1' and len(js['geocodes']) != 0:
        location = js['geocodes'][0]['location']
        location_arr = location.split(',')
        location = "%.4f,%.4f" % (float(location_arr[1]), float(location_arr[0]))
        darksky_key = "c0930b16e7d43d90e3770bf306c25260"
        darksky_url = "https://api.darksky.net/forecast/%s/%s?lang=zh" % (darksky_key, location)
        con1 = requests.get(darksky_url)
        print(con1.content)
        js1 = json.loads(con1.content)
        return "%s: 即时天气 %s 实时温度 %.2f 体感温度 %.2f 降水概率 %d%% 湿度 %d %% " \
               % (nick, js1['currently']['summary'], js1['currently']['temperature'], js1['currently']['apparentTemperature'],
                  js1['currently']['precipProbability']*100, js1['currently']['humidity']*100)
    else:
        return "%s: 城市输入有误" % nick