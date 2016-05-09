# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------

import os
PLUGINDIR = './plugins/'


def load_plugins():
    plugins = os.listdir(PLUGINDIR)
    list1 = list()
    list2 = list()
    handlers = list()
    for plugin in plugins:
        exec("from .plugins." + plugin + " import *")
        if plugin.lower().endswith('handler'):
            handlers.append(plugin)
        else:
            list1.append(plugin)
            list2.extend(dir(plugin))
    return list1, list2, handlers

