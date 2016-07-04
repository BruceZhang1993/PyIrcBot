# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------

'''ip lookup plugin'''
import re
import json
import requests

def ip(args, nick, channel, c, e):
    if not args:
        return _getip(e.source.host)
    else:
        return False


def _getip(ip):
    if re.match(r'\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}', ip):
        ret = requests.get("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=%s" % ip)
        jret = json.loads(ret.text)
        return "%s %s %s %s %s" % (jret['country'], jret['province'], jret['city'], jret['district'], jret['isp'])
    else:
        return "查询失败！检查是否已隐身！"