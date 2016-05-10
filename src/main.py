# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------

import irc.bot
import os
import json
import logging
from termcolor import colored
import re
import sys
import signal

PREFIX = '>>'
PLUGINDIR = './plugins/'

sys.path.append(PLUGINDIR)

from echo import echo
from linkhandler import linkhandler

pluginlist = ["echo"]
handlerlist = ["linkhandler"]
funclist = [echo]
handlerfuncs = [linkhandler]


class MyBot(irc.bot.SingleServerIRCBot):

    version = "201605-dev"

    def __init__(self, channels, nickname, server, port, realname):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)],
                                            nickname, realname)
        self.chs = channels
        logger.info("Bot started successfully.")
        signal.signal(signal.SIGINT, self._quit)

    def _quit(self):
        logger.info("Bot interuptted from console.")
        self.die("Bot stopped from console.")

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        for channel in self.chs:
            c.join(channel)

    def on_kick(self, c, e):
        channel = e.target
        c.join(channel)

    def exec_command(self, commandline):
        cmdargs = commandline.split(' ', 1)
        if cmdargs[0] in pluginlist:
            index = pluginlist.index(cmdargs[0])
            msg = funclist[index](cmdargs[1])
            return msg
        return False

    def passive_exec(self, line, nick='', channel=''):
        for handler in handlerlist:
            index = handlerlist.index(handler)
            resmsg = handlerfuncs[index](line, nick, channel)
            return resmsg

    def on_privmsg(self, c, e):
        nm = e.source
        line = e.arguments[0]
        if line.startswith(PREFIX):
            commandline = line.strip(PREFIX).strip()
            msg = self.exec_command(commandline)
            if msg:
                c.privmsg(nm.nick, msg)
        else:
            msg = self.passive_exec(line, nm.nick)
            if msg:
                c.privmsg(nm.nick, msg)

    def on_pubmsg(self, c, e):
        nick = e.source.nick
        channel = e.target
        line = e.arguments[0]
        if line.startswith(PREFIX):
            commandline = line.strip(PREFIX).strip()
            msg = self.exec_command(commandline)
            if msg:
                c.privmsg(channel, "%s: %s" % (nick, msg))
        else:
            msg = self.passive_exec(line, nick, channel)
            if msg:
                c.privmsg(channel, "%s" % msg)

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        pass

    def on_dccchat(self, c, e):
        pass

    def get_version(self):
        return "PyIrcBot | https://github.com/BruceZhang1993/PyIrcBot | Version: %s" % self.version


def _do_nothing():
    pass


def main():
    # DONE:10 Try using config file
    confdir = os.environ['HOME'] + "/.pyircbot/"
    conffile = confdir + "config.json"
    logfile = confdir + "bot.log"

    try:
        os.mkdir(confdir)
    except FileExistsError:
        _do_nothing()

    # Logging
    global logger
    logger = logging.getLogger("ircbot")
    logger.setLevel(logging.DEBUG)
    logfilehandler = logging.FileHandler(logfile)
    logfilehandler.setLevel(logging.DEBUG)
    logfilehandler.setLevel(logging.NOTSET)
    consolehandler = logging.StreamHandler()
    consolehandler.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(msg)s (%(name)s)")
    consolehandler.setFormatter(formatter)
    logfilehandler.setFormatter(formatter)
    logger.addHandler(consolehandler)
    logger.addHandler(logfilehandler)

    if os.path.exists(conffile):
        logger.debug("Configure file found. Using now...")
        fp = None
        try:
            fp = open(conffile, "r")
            config = json.load(fp)
            channels = config["channels"]
            nickname = config["nick"]
            server = config["network"]
            port = config["port"]
            realname = config["realname"]
        except IOError:
            logger.error("I/O Error. Check filesystem permissions.")
            import sys
            sys.exit(1)
        finally:
            if fp:
                fp.close()
        logger.debug("Configure file loaded. Starting bot...")
    else:
        logger.info("Configure file not found. Creating now...")
        print(colored("-- PyIrcBot 配置向导 --", "yellow"))
        config = dict()
        config['nick'] = input(colored("Nickname: ", "green")).strip()
        config["realname"] = input(colored("Real Name: ", "green")).strip()
        print(colored("-- 配置 IRC 服务器 --", "blue"))
        config['network'] = input(colored("Server: ", "green")).strip()
        config['port'] = int(input(colored("Port: ", "green")).strip())
        config['channels'] = re.split(r'\s+', input(colored("Channels (Split with space): ", "green")))
        fp = None
        try:
            fp = open(conffile, "w")
            json.dump(config, fp)
        except IOError:
            logger.error("I/O Error. Check filesystem permissions.")
            import sys
            sys.exit(1)
        finally:
            if fp:
                fp.close()
        logger.debug("Configure file created. Starting bot...")
        print(colored("配置文件创建成功，启动 PyIrcBot...", "yellow"))
        channels = config["channels"]
        nickname = config["nick"]
        server = config["network"]
        port = config["port"]
        realname = config["realname"]
    logger.info("Loading plugins...")
    bot = MyBot(channels, nickname, server, port, realname)
    bot.start()

if __name__ == "__main__":
    main()
