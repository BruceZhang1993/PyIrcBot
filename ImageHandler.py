#!/usr/bin/env python3
# encoding=utf-8
import urllib.request
import urllib.error
import urllib.parse
from PIL import Image


class ImageHandler(object):
    def __init__(self, url):
        # TODO Read 1000 bytes
        self.url = url
        try:
            self.r = urllib.request.Request(self.url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"})
            self.file = urllib.request.urlopen(self.r)
            self.image = Image.open(self.file)
        except:
            self.image = False

    def get_format(self, lower=False):
        if self.image:
            if lower:
                return self.image.format.lower()
            return self.image.format
        return False

    def get_size(self, formats="Width: %W Height: %H"):
        if self.image:
            (width, height) = self.image.size
            return formats.replace("%W", str(width)).replace("%H", str(height))
        return False

    def get_mode(self, lower=False):
        if self.image:
            if lower:
                return self.image.mode.lower()
            return self.image.mode
        return False
