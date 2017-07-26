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
                    if module.__name__ == arg1:
                        importlib.reload(module)
                        break;
                # exec("global %s" % arg1)
                exec("%s=getattr(module, arg1)" % arg1)
                return "%s: Plugin `%s` reloaded." % (nick, arg1)
            except:
                return "%s: Plugin `%s` not found." % (nick, arg1)
    return "%s: Not admin."
