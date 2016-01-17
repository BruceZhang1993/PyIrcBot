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
        try:
            self.r = requests.get(self.url, headers=self.head)
        except Exception:
            self.r = False
        # self.detect_encoding()

    def get_title(self):
        if self.r:
            soup = BeautifulSoup(self.r.content, "html5lib")
            # print(soup.original_encoding)
            if soup.title:
                return soup.title.string
            else:
                return False
        return False

if __name__ == '__main__':
    th = TitleHandler("http://hb.qq.com")
    print(th.get_title())
