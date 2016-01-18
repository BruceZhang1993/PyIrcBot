#!/usr/bin/env python3
# encoding=utf-8
import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import chardet
import re


class TitleHandler(object):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
    }
    charset = None
    soup = None

    def __init__(self, url):
        self.url = url
        try:
            self.r = requests.get(self.url, headers=self.head)
            ct = self.r.headers.get("content-type")
            matches = re.match(r'charset\=([\w\-]+)', ct, re.IGNORECASE)
            if matches and matches.group(1).lower() != "utf-8":
                self.charset = matches.group(1)
        except Exception:
            self.r = False
        if self.r:
            self.soup = BeautifulSoup(self.r.content, "html5lib", from_encoding=self.charset)
        # self.detect_encoding()

    def get_title(self):

        if self.soup and self.soup.title:
            return self.soup.title.string
        else:
            return False

    def get_charset(self, upper=True):
        if self.soup:
            if upper:
                return self.soup.original_encoding.upper()
            else:
                return self.soup.original_encoding
        else:
            return False


if __name__ == '__main__':
    th = TitleHandler("http://hb.qq.com")
    print(th.get_title())
