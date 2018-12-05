# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# IP lookup plugins - Sina API
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------

import json
import requests

def ip(args, nick, channel, c, e):
    if not args:
        return "%s: %s" % (nick, _getip(e.source.host))
    else:
        return "%s: %s" % (nick, _getip(args))


def _getip(ip):
    try:
        ret = requests.get("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=%s" % ip)
        jret = json.loads(ret.text)
        return "%s %s %s %s %s" % (jret['country'], jret['province'], jret['city'], jret['district'], jret['isp'])
    except Exception as e:
        return "未知错误"
