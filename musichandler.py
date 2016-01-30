#!/usr/bin/env python3
# encoding=utf-8

import requests
import json
# http://music.163.com/api/song/detail/?id=33579017&ids=["33579017"]


def netease(song_id):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
    }
    req = requests.get('http://music.163.com/api/song/detail/?id=%s&ids=["%s"]' % (song_id, song_id), headers=head)
    response = json.loads(req.text)
    return (response["songs"][0]["name"], response["songs"][0]["artists"][0]["name"], response["songs"][0]["mp3Url"])

if __name__ == '__main__':
    print(netease("33579017"))
