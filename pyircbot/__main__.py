# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------

import irc.bot
import irc.client
import irc.buffer
import os
import json
import logging
from termcolor import colored
import re
import sys
import signal
import importlib
from os.path import splitext
import pyircbot.globalvar

logger = logging.getLogger('ircbot')
PLUGINDIR = './plugins/'
PREFIX = '$'

plugins = list(map(lambda file: splitext(file)[0] ,filter(lambda file: file.endswith('.py') and not file.startswith('__init__'), os.listdir(PLUGINDIR))))
pluginss = []
pyircbot.globalvar.modules = []
for plugin in plugins:
    try:
        module = importlib.import_module("plugins.%s" % plugin)
        pyircbot.globalvar.modules.append(module)
        exec("pyircbot.globalvar.%s=getattr(module, plugin)" % plugin)
        pluginss.append(plugin)
    except ImportError as e:
        print(e);
        logger.warning("Cannot load plugin `%s`, ignoring it." % plugin)

# from plugins.echo import echo
# from plugins.ip import ip
# from plugins.linkhandler import linkhandler

class MyBot(irc.bot.SingleServerIRCBot):

    version = "201606-dev"

    def __init__(self, channels, nickname, server, port, realname):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)],
                                            nickname, realname)
        pyircbot.globalvar.handlers = list(filter(lambda p: p.endswith('handler'), pluginss))
        pyircbot.globalvar.commands = list(filter(lambda p: not p.endswith('handler'), pluginss))
        self.chs = channels
        logger.info("Bot started successfully.")
        signal.signal(signal.SIGINT, self._quit)

    def _quit(self, arg1, arg2):
        logger.info("Bot interuptted from console.")
        msg = input("The reason for stopping bot: ")
        self.die(msg or "")

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        for channel in self.chs:
            c.join(channel)

    def on_kick(self, c, e):
        channel = e.target
        c.join(channel)

    def exec_command(self, commandline, nick='', channel='', con=False, event=False):
        cmdargs = commandline.split(' ', 1)
        if cmdargs[0] == 'help':
            return self._helpmsg(nick)
        if cmdargs[0] in pyircbot.globalvar.commands:
            if len(cmdargs) < 2:
                args = ''
            else:
                args = cmdargs[1]
            msg = eval("pyircbot.globalvar.%s" % cmdargs[0])(args, nick, channel, con, event)
            return msg
        return False

    def _helpmsg(self, nick):
        return "%s: 已加载插件列表 [ %s ] | 主动技能 [ %s ] | 被动技能 [ %s ]" % ( nick, ','.join(list(filter(lambda x:"`%s`" % x, plugins))), ','.join(list(filter(lambda x:"`%s`" % x, pyircbot.globalvar.commands))),','.join(list(filter(lambda x:"`%s`" % x, pyircbot.globalvar.handlers))))

    def passive_exec(self, line, nick='', channel='', con=False, event=False):
        if line.strip().endswith(" #"):
            return []
        for handler in pyircbot.globalvar.handlers:
            resmsg = eval("pyircbot.globalvar.%s" % handler)(line, nick, channel, con, event)
            return resmsg

    def on_privmsg(self, c, e):
        nm = e.source
        line = e.arguments[0]
        try:
            if line.startswith(PREFIX):
                commandline = line.strip(PREFIX).strip()
                msg = self.exec_command(commandline, nm.nick, con=c, event=e)
                if msg:
                    c.privmsg(nm.nick, msg)
            else:
                msgs = self.passive_exec(line, nm.nick, con=c, event=e)
                for msg in msgs:
                    if msg:
                        c.privmsg(nm.nick, msg)
        except irc.client.InvalidCharacters:
            logger.warning("Invalid characters sent.")
            _do_nothing()

    def on_pubmsg(self, c, e):
        nick = e.source.nick
        channel = e.target
        line = e.arguments[0]
        try:
            if line.startswith(PREFIX):
                commandline = line.strip(PREFIX).strip()
                msg = self.exec_command(commandline, nick, channel, con=c, event=e)
                if msg:
                    c.privmsg(channel, msg)
            else:
                msgs = self.passive_exec(line, nick, channel, con=c, event=e)
                for msg in msgs:
                    if msg:
                        c.privmsg(channel, "%s" % msg)
        except irc.client.InvalidCharacters:
            logger.warning("Invalid characters sent.")
            _do_nothing()

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        pass

    def on_dccchat(self, c, e):
        pass

    def get_version(self):
        return "PyIrcBot | https://github.com/BruceZhang1993/PyIrcBot | Version: %s" % self.version


def _do_nothing():
    pass


class IgnoreErrorsBuffer(irc.buffer.DecodingLineBuffer):
    def handle_exception(self):
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
    logfilehandler.setLevel(logging.NOTSET)
    consolehandler = logging.StreamHandler()
    consolehandler.setLevel(logging.NOTSET)
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
    irc.client.ServerConnection.buffer_class = IgnoreErrorsBuffer
    bot.start()


if __name__ == "__main__":
    main()
