#!/usr/bin/env python3
# encoding=utf-8
import urllib.request
import urllib.error
import urllib.parse
from PIL import Image


class ImageHandler(object):
    def __init__(self, url):
        self.url = url
        self.file = urllib.request.urlopen(self.url)
        self.image = Image.open(self.file)

    def get_format(self, lower=False):
        if lower:
            return self.image.format.lower()
        return self.image.format

    def get_size(self, formats="Width: %W Height: %H"):
        (width, height) = self.image.size
        return formats.replace("%W", str(width)).replace("%H", str(height))

    def get_mode(self, lower=False):
        if lower:
            return self.image.mode.lower()
        return self.image.mode
