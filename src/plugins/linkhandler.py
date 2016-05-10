# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------
import re
import requests
import sys
import urllib.request
import urllib.error
import urllib.parse
from PIL import Image
sys.path.append("../")
from bs4 import BeautifulSoup

fake_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}


def linkhandler(line, nick, channel):
    global logger
    words = line.split()
    for word in words:
        if _is_httplink(word) and not _is_localnet(word):
            ftype, length = _get_url_info(word)
            if ftype == "" and length == 0:
                return ""
            elif length == -1:
                return "Connection Timeout."
            elif ftype.startswith("text/html"):
                return "↑↑ Title: " + _get_url_title(word) + " ↑↑"
            elif ftype.startswith("image"):
                size, unit = _parse_filesize(length)
                imgtype, reso = _get_img_reso(word)
                return "↑↑ [ %s (%s) ] %.2f%s %s ↑↑" % (imgtype, ftype, size, unit, reso)
            else:
                size, unit = _parse_filesize(length)
                return "↑↑ [ %s ] %.2f%s ↑↑" % (ftype, size, unit)


def _parse_filesize(bytes):
    bytes = float(bytes)
    sizes = ["Bytes", "KB", "GB", "TB"]
    index = 0
    while bytes > 1000:
        bytes /= 1024.0
        index += 1
    return bytes, sizes[index]


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
    global logger
    try:
        req = requests.head(url, headers=fake_headers, timeout=10)
        return req.headers.get("content-type", ""), req.headers.get("content-length", 0)
    except requests.ConnectTimeout:
        #logger.warning("Connection timeout while getting URL info.")
        return "", -1
    except:
        #logger.warning("Error getting URL info.")
        return "", 0


def _get_url_title(url):
    global logger
    try:
        req = requests.get(url, headers=fake_headers, timeout=10)
        soup = BeautifulSoup(req.content, "html5lib")
        if soup and soup.title:
            return soup.title.string
    except requests.ConnectTimeout:
        #logger.warning("Connection timeout while getting URL title.")
        return ""
    except:
        #logger.warning("Error getting URL title.")
        return ""


def _formatted_size(size):
    width, height = size
    return "%d x %d" % (width, height)


def _get_img_reso(url):
    r = urllib.request.Request(url, headers=fake_headers)
    file = urllib.request.urlopen(r)
    image = Image.open(file)
    return image.format.upper(), _formatted_size(image.size)


