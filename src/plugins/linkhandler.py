# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------
import re
import requests
from bs4 import BeautifulSoup

fake_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}


def linkhandler(line, nick, channel):
    words = line.split()
    if _is_httplink(words) and not _is_localnet(words):
        type, length = _get_url_info(words)


def _is_httplink(words):
    return re.match(r'https?://', words)


def _is_localnet(words):
    if words.find("127.0.0.1") != -1:
        return True
    elif words.find("localhost") != -1:
        return True
    elif words.find("192.168.") != -1:
        return True
    else:
        return False

def _get_url_info(url):
    req = requests.head(url, headers=fake_headers)
    return req.headers.get("content-type", ""), req.headers.get("content-length", 0)