# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------
# License: The MIT License (MIT)
# Copyright (c) 2015 Bruce Zhang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad
import json
from time import strftime
from timeloop import TimeLoop
import re
from bs4 import BeautifulSoup
import requests
import chardet
from ImageHandler import ImageHandler
from random import randint


class MyBot(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port, admins):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)],
                                            nickname, nickname)
        self.channel = channel
        self.timer = TimeLoop(1, self.time_func)
        self.admins = admins
        # TODO:10 More channels support

    def time_func(self):
        msgs = [
            "0点了，再不碎觉，饥佬们小心不生精啊，腐女们小心会平胸哦!",
            "1点了，还没有睡？正是发福利的好时间!",
            "2点了，这个点还没睡觉，注定孤独一生!",
            "3点了，3点了，碎觉碎觉!",
            "4点了，你是起床了还是还没睡呢？注意身体哦!",
            "5点了，5点了，早起的虫子有鸟吃!",
            "6点了，呦，呦，切克闹，煎饼果子来一套!",
            "7点了，正是来一发的好钟点!",
            "8点了，都8点了，我和我的小伙伴们都惊呆了!",
            "9点了，时间过的好快，快的我都快睡着了!",
            "10点了，00后表示，什么时候才放学啊!",
            "11点了，这个点是该想想中午该吃点啥了!",
            "12点了，酒足饭饱思淫欲，正是调戏妹纸的好时间!",
            "13点了，这个点不午睡都对不起普天百姓，碎觉!",
            "14点了，哎呀，还想再睡一会，哎，可是一个人睡太无聊了!",
            "15点了，请妹纸们喝茶了饥佬们!",
            "16点了，晚饭吃点什么呢？",
            "17点了，16点你丫就开始想着吃晚饭了，吃货注孤生!",
            "18点了，现在是该想想吃点什么了!",
            "19点了，我是该看电视剧还是上irc？",
            "20点了，又是一天，反反复复，一人吃饱，全家不饿!",
            "21点了，贴吧水两贴去吧!",
            "22点了，来点福利吧!",
            "23点了，往事历历在目，让我终于醒悟，光棍还是很有前途，跟着狐朋狗友大家抽烟喝酒，一玩一宿，不用发愁!"
        ]
        smileys = ["_(:3 」∠)_", "(ง •̀_•́)ง", "(┙>∧<)┙へ┻┻", "Σ( ° △ °|||)︴",
                   "(→_→)", "(＞д＜)", "(┬＿┬)", "╮（╯＿╰）╭"]
        hour = int(strftime("%H"))
        minute = int(strftime("%M"))
        sec = int(strftime("%S"))
        if minute == 0 and sec == 0:
            choose = randint(0, len(smileys) - 1)
            self.connection.action(self.channel, smileys[choose] + " " +
                                   msgs[hour])

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        self.timer.start()

    def on_privmsg(self, c, e):
        pass

    def on_pubmsg(self, c, e):
        self.url_detect(e.arguments[0])
        # Following condition only matches when $ at the beginning
        if e.arguments[0][0] == "$":
            a = e.arguments[0][1:]
            self.do_command(e, a)

    def url_detect(self, msg):
        words = msg.split()
        for word in words:
            if self.is_url(word):
                if self.is_image(word):
                    image = ImageHandler(word)
                    imtype = image.get_format()
                    imsize = image.get_size("%W x %H")
                    self.connection.privmsg(
                        self.channel,
                        "[ Image ] 类型: %s 尺寸: %s" % (imtype, imsize))
                else:
                    title = self.get_title(word)
                    if title:
                        try:
                            self.connection.privmsg(self.channel,
                                                    "[ %s ] %s" % (title, word))
                        except irc.client.InvalidCharacters:
                            pass

    def is_url(self, url):
        return re.match(r'^https?:\/\/', url)

    def is_image(self, url):
        return False      # disable for now
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
        }
        try:
            r = requests.get(url, headers=head)
        except requests.exceptions.ConnectionError:
            print("Connection Faild.")
            return False
        mime = r.headers.get("Content-Type")
        if mime.find("image") != -1:
            # self.connection.privmsg(self.channel, "Content-Type: %s" % mime)
            return True
        return False

    def get_title(self, url):
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
        }
        r = requests.get(url, headers=head)
        if r.headers.get("content-type").find("html") != -1:
            ctype = r.headers.get("content-type")
            if ctype.find("charset") != -1:
                pos = ctype.find("charset") + 8
                r.encoding = ctype[pos:]
            elif r.text.find("charset=\"") != -1:
                matches = re.match(r'charset=\"(\w+)\"', r.text)
                if matches:
                    r.encoding = matches.group(1)
            elif r.text.find("charset=") != -1:
                matches = re.match(r'charset=(\w+)', r.text)
                if matches:
                    r.encoding = matches.group(1)
            else:
                r.encoding = chardet.detect(r.raw.read())["encoding"]
            soup = BeautifulSoup(r.text, "html5lib")
            return soup.title.string
        return False

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        text = e.arguments[0].decode('utf-8')
        c.privmsg("You said: " + text)

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection
        cmd_args = cmd.split()
        cmd = cmd_args[0]
        args = " ".join(cmd_args[1:])
        self.execute_command(cmd, args, nick, self.channel)

    def execute_command(self, cmd, args, nick, channel):
        # DONE:0 Finish function command_string
        # TODO:0 More commands and command interface
        ctime = strftime("%Y-%m-%d %H:%M:%S")
        simplecommands = {
            "say": "%s wanted me to say: %s" % (nick, args),
            "time": "%s: Current time is %s" % (nick, ctime)
        }

        c = self.connection
        if cmd in simplecommands.keys():
            c.privmsg(self.channel, simplecommands[cmd])
        elif cmd == "quit":
            if nick in self.admins:
                c.quit("admin %s asked me to quit." % nick)
                sys.exit(0)
            else:
                c.privmsg(self.channel,
                          "%s: You're not one of the admins." % nick)
        else:
            return False


def main():
    # DONE:10 Try using config file
    fp = None
    try:
        fp = open('config.json', "r")
        config = json.load(fp)
        channel = config["channel"]
        nickname = config["nick"]
        server = config["network"]
        port = config["port"]
        admins = config["admins"]
    except IOError:
        print("I/O Error.")
        import sys
        sys.exit(1)
    finally:
        if fp:
            fp.close()
    bot = MyBot(channel, nickname, server, port, admins)
    bot.start()

if __name__ == "__main__":
    main()
