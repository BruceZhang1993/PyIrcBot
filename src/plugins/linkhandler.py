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
    results = []
    for word in words:
        if _is_httplink(word) and not _is_localnet(word):
            if word.find('music.163.com') != -1:
                word = _nemusic_reformat(word)
            ftype, length = _get_url_info(word)
            if ftype == "" and length == 0:
                results.append("")
            elif length == -1:
                results.append(_colored("Connection Timeout.", "yellow"))
            elif ftype.startswith("text/html"):
                title = _get_url_title(word)
                if title:
                    results.append(_colored("↑↑ Title: ", "blue") + _colored(title, "orange") + _colored(" ↑↑", "blue"))
                else:
                    size, unit = _parse_filesize(length)
                    results.append(_colored("↑↑ [ %s ] %.2f%s ↑↑" % (ftype, size, unit), "blue"))
            elif ftype.startswith("image"):
                size, unit = _parse_filesize(length)
                imgtype, reso = _get_img_reso(word)
                results.append(_colored("↑↑ [ %s (%s) ] %.2f%s %s ↑↑" % (imgtype, ftype, size, unit, reso), "blue"))
            else:
                size, unit = _parse_filesize(length)

                results.append(_colored("↑↑ [ %s ] %.2f%s ↑↑" % (ftype, size, unit), "blue"))
    return results


def _parse_filesize(bytes):
    bytes = float(bytes)
    sizes = ["Bytes", "KB", "MB", "GB", "TB"]
    index = 0
    while bytes > 1000:
        bytes /= 1024.0
        index += 1
    return bytes, sizes[index]


def _nemusic_reformat(url):
    return ''.join(url.split('#/'))


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
        logger.debug("HEAD %s HTTP %d" % (url, headreq.status_code))
        headreq.raise_for_status()
        # if headreq.headers.get("content-length", False):
        #     yield Exception

        return headreq.headers.get("content-type", "unknown"), headreq.headers.get("content-length", 0)
    except:
        try:
            req2 = requests.get(url, headers=fake_headers, timeout=20, allow_redirects=True)
            logger.debug("GET %s HTTP %d" % (url, req2.status_code))
            req2.raise_for_status()
            return req2.headers.get("content-type", "unknown"), len(req2.text)
        except:
            logger.warning("Error getting URL info for %s." % url)
            return "", 0


def _get_url_title(url):
    global logger
    try:
        req2 = requests.get(url, headers=fake_headers, timeout=20)
        logger.debug("GET %s HTTP %d" % (url, req2.status_code))
        req2.raise_for_status()
        soup = BeautifulSoup(req2.content, "html5lib")
        if soup and soup.title:
            return soup.title.string
    except:
        logger.warning("Error getting URL title for %s" % url)
        return "", 0


def _formatted_size(size):
    width, height = size
    return "%d x %d" % (width, height)


def _get_img_reso(url):
    r = urllib.request.Request(url, headers=fake_headers)
    file = urllib.request.urlopen(r)
    image = Image.open(file)
    return image.format.upper(), _formatted_size(image.size)


