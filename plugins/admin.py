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
                    if module.__name__ == 'plugins.' + arg1.strip():
                        importlib.reload(module)
                        exec("pyircbot.globalvar.%s=getattr(module, arg1)" % arg1)
                        break;
                # exec("global %s" % arg1)
                return "%s: Plugin `%s` reloaded." % (nick, arg1)
            except Exception as e:
                logger.debug(e);
                return "%s: Plugin `%s` not found." % (nick, arg1)
        elif subcommand == 'reloadall':
            try:
                for module in pyircbot.globalvar.modules:
                    importlib.reload(module)
                    exec("pyircbot.globalvar.%s=getattr(module, arg1)" % arg1)
                # exec("global %s" % arg1)
                return "%s: All Plugins reloaded." % (nick)
            except Exception as e:
                logger.debug(e);
    return "%s: Not admin." % nick
