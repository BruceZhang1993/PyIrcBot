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
import logging
from PIL import Image
sys.path.append("../")
from bs4 import BeautifulSoup

fake_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}
logger = logging.getLogger("ircbot")


def linkhandler(line, nick, channel):
    words = line.split()
    for word in words:
        if _is_httplink(word) and not _is_localnet(word):
            ftype, length = _get_url_info(word)
            if ftype == "" and length == 0:
                return ""
            elif length == -1:
                return _colored("Connection Timeout.", "yellow")
            elif ftype.startswith("text/html"):
                title = _get_url_title(word)
                if title:
                    return _colored("↑↑ Title: ", "blue") + _colored(title, "orange") + _colored(" ↑↑", "blue")
                else:
                    size, unit = _parse_filesize(length)
                    return _colored("↑↑ [ %s ] %.2f%s ↑↑" % (ftype, size, unit), "blue")
            elif ftype.startswith("image"):
                size, unit = _parse_filesize(length)
                imgtype, reso = _get_img_reso(word)
                return _colored("↑↑ [ %s (%s) ] %.2f%s %s ↑↑" % (imgtype, ftype, size, unit, reso), "blue")
            else:
                size, unit = _parse_filesize(length)

                return _colored("↑↑ [ %s ] %.2f%s ↑↑" % (ftype, size, unit), "blue")


def _parse_filesize(bytes):
    bytes = float(bytes)
    sizes = ["Bytes", "KB", "MB", "GB", "TB"]
    index = 0
    while bytes > 1000:
        bytes /= 1024.0
        index += 1
    return bytes, sizes[index]


def _colored(text, forecolor):
    colordict = {
        "white": "00",
        "black": "01",
        "blue": "02",
        "green": "03",
        "red": "04",
        "brown": "05",
        "purple": "06",
        "orange": "07",
        "yellow": "08"
    }
    if forecolor.lower() in colordict.keys():
        return "\x03%s%s\x03" % (colordict.get(forecolor.lower()), text)
    else:
        return text


def _is_httplink(words):
    return re.match(r'^https?://', words)


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
        headreq = requests.head(url, headers=fake_headers, timeout=20, allow_redirects=True)
        if headreq.status_code == 200 and headreq.headers.get("content-length", False):
            return headreq.headers.get("content-type", "unknown"), headreq.headers.get("content-length", 0)
        elif headreq.status_code == 200:
            req2 = requests.get(url, headers=fake_headers, timeout=20, allow_redirects=True)
            return req2.headers.get("content-type", "unknown"), len(req2.text)
        else:
            logger.warning("Error getting URL info for %s." % url)
            return "", 0
    except:
        logger.warning("Error getting URL info for %s." % url)
        return "", 0


def _get_url_title(url):
    global logger
    try:
        req = requests.get(url, headers=fake_headers, timeout=20)
        soup = BeautifulSoup(req.content, "html5lib")
        if soup and soup.title:
            return soup.title.string
    except:
        logger.warning("Error getting URL title for %s" % url)
        return ""


def _formatted_size(size):
    width, height = size
    return "%d x %d" % (width, height)


def _get_img_reso(url):
    r = urllib.request.Request(url, headers=fake_headers)
    file = urllib.request.urlopen(r)
    image = Image.open(file)
    return image.format.upper(), _formatted_size(image.size)


