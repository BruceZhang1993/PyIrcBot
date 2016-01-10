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
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import json
from time import strftime
from timeloop import TimeLoop
import re
from bs4 import BeautifulSoup
import requests
import chardet
from ImageHandler import ImageHandler


class MyBot(irc.bot.SingleServerIRCBot):
    admins = ["bruceutut", "bruceutut-m"]

    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)],
                                            nickname, nickname)
        self.channel = channel
        self.timer = TimeLoop(1, self.time_func)
        # TODO:10 More channels support

    def time_func(self):
        hour = int(strftime("%H"))
        minute = int(strftime("%M"))
        sec = int(strftime("%S"))
        if minute == 0 and sec == 0:
            self.connection.action(self.channel, "It's %d o'clock now!" % hour)

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
        a = e.arguments[0].split('$')
        if len(a) > 1 and a[0] == "":
            self.do_command(e, a[1].strip())

    def url_detect(self, msg):
        words = msg.split()
        for word in words:
            if self.is_url(word):
                if self.is_image(word):
                    image = ImageHandler(word)
                    imtype = image.get_format()
                    imsize = image.get_size("%W x %H")
                    self.connection.privmsg(self.channel, "[ Image ] 类型: %s 尺寸: %s" % (imtype, imsize))
                else:
                    title = self.get_title(word)
                    if title:
                        self.connection.privmsg(self.channel, "[ %s ] %s" % (title, word))

    def is_url(self, url):
        return re.match(r'^https?:\/\/', url)

    def is_image(self, url):
        return re.match(r'\.jpg$|\.png$|\.ico$|\.gif$|\.tiff$|\.jpeg$|\.bmp$|\.svg$|\.tga$', url, re.IGNORECASE)

    def get_title(self, url):
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
        }
        r = requests.get(url, headers = head)
        r.encoding = chardet.detect(r.text.encode())["encoding"]
        soup = BeautifulSoup(r.text, "html5lib")
        return soup.title.string

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
        simplecommands = {
            "say": "%s wanted me to say: %s" % (nick, args)
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
    except IOError:
        print("I/O Error.")
        import sys
        sys.exit(1)
    finally:
        if fp:
            fp.close()
    bot = MyBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
