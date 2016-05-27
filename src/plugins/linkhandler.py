# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------
import logging
import re
import sys

import requests
from PIL import Image

sys.path.append("../")
from bs4 import BeautifulSoup

fake_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}
logger = logging.getLogger("ircbot")


def linkhandler(line, nick, channel):
    # logger.debug('public msg received: %s' % line)
    words = line.split()
    results = []
    for word in words:
        if _is_httplink(word) and not _is_localnet(word):
            con = None
            if word.find('music.163.com') != -1:
                word = _nemusic_reformat(word)
            try:
                con = requests.get(word, stream=True, allow_redirects=True)
                con.raise_for_status()
            except:
                code = "Unknown"
                if con is not None:
                    code = str(con.status_code)
                logger.warning("Connection failed for %s Error: %s" % (word, code))
                continue
            ftype, length = _get_url_info(con)
            if ftype == "" and length == 0:
                results.append("")
            elif length == -1:
                results.append(_colored("Connection Timeout.", "yellow"))
            elif ftype.startswith("text/html"):
                title = _get_url_title(con)
                if title:
                    results.append(_colored("↑↑ Title: ", "blue") + _colored(title, "orange") + _colored(" ↑↑", "blue"))
                else:
                    size, unit = _parse_filesize(length)
                    results.append(_colored("↑↑ [ %s ] %.2f%s ↑↑" % (ftype, size, unit), "blue"))
            elif ftype.startswith("image"):
                size, unit = _parse_filesize(length)
                imgtype, reso, mode = _get_img_reso(con)
                results.append(_colored("↑↑ [ %s ] %.2f%s %s %s ↑↑" % (imgtype, size, unit, reso, mode), "blue"))
            else:
                size, unit = _parse_filesize(length)
                results.append(_colored("↑↑ [ %s ] %.2f%s ↑↑" % (ftype, size, unit), "blue"))
                con.close()
            if con is not None:
                con.close()
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


def _get_url_info(con):
    type = con.headers.get('content-type', 'unknown')
    length = con.headers.get('content-length', 0)
    return type, length


def _get_url_title(con, maxlen=5000):
    lines = []
    for line in con.iter_lines():
        lines.append(line)
        if str(line).find('</title>') != -1:
            con.close()
            con = None
            return BeautifulSoup(b''.join(lines), 'html5lib').title.text
        if str(line).find('</head>') != -1:
            con.close()
            con = None
            return False
        if len(lines) >= maxlen:
            con.close()
            con = None
            break
    return False


def _formatted_size(size):
    width, height = size
    return "%d x %d" % (width, height)


def _get_img_reso(con):
    image = Image.open(con.raw)
    return image.format.upper(), _formatted_size(image.size), image.mode
