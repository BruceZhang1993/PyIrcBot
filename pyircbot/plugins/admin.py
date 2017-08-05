# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------

import importlib
import logging
import pyircbot.globalvar

'''admin management plugin'''
logger = logging.getLogger('ircbot')

def admin(args, nick, channel, c, e):
    nm = e.source
    if nm.nick == 'bruceutut' and nm.host == 'unaffiliated/bruceutut':
        cmd = args.split(' ', 1)
        if len(cmd) == 0:
            return False
        subcommand = cmd[0]
        arg1 = False
        if len(cmd) >= 2:
            arg1 = cmd[1]
        if subcommand == 'reload' and arg1 is not False:
            try:
                for module in pyircbot.globalvar.modules:
                    if module.__name__ == 'pyircbot.plugins.' + arg1.strip():
                        importlib.reload(module)
                        exec("pyircbot.globalvar.%s=getattr(module, arg1)" % arg1)
                        break
                # exec("global %s" % arg1)
                return "%s: 插件 `%s` 已重新加载" % (nick, arg1)
            except Exception as e:
                logger.debug(e)
                return "%s: 插件 `%s` 不存在" % (nick, arg1)
        elif subcommand == 'reloadall':
            try:
                for module in pyircbot.globalvar.modules:
                    importlib.reload(module)
                    exec("pyircbot.globalvar.%s=getattr(module, module.__name__.split('.')[1]))" % (module.__name__.split('.')[1]))
                # exec("global %s" % arg1)
                return "%s: 所有插件已重新加载" % (nick)
            except Exception as e:
                logger.debug(e)
        elif subcommand == 'load' and arg1 is not False:
            try:
                module = importlib.import_module("pyircbot.plugins.%s" % arg1)
                pyircbot.globalvar.modules.append(module)
                exec("pyircbot.globalvar.%s=getattr(module, arg1)" % arg1)
                return "%s: 插件 `%s` 已成功加载" % (nick, arg1)
            except Exception as e:
                logger.debug(e);
                return "%s: 插件 `%s` 加载失败" % (nick, arg1)
    return "%s: 不是管理用户" % nick
