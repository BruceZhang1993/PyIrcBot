#!/usr/bin/env python3
# encoding=utf-8
import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import chardet


class TitleHandler(object):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
    }

    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url, headers=self.head)
        # self.detect_encoding()

    def get_title(self):
        soup = BeautifulSoup(self.r.content, "html5lib")
        # print(soup.original_encoding)
        return soup.title.string

if __name__ == '__main__':
    th = TitleHandler("http://hb.qq.com")
    print(th.get_title())
