# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------

import os
#import importlib
import logging

logger = logging.getLogger('ircbot')

def load_plugins(plugin_dir):
    plugins = list(map(lambda file: file.strip('.py') ,filter(lambda file: file.endswith('.py') and not file.startswith('__init__'), os.listdir(plugin_dir))))
    loaded_plugins = []
    for plugin in plugins:
        try:
            #importlib.import_module('plugins.%s' % plugin)
            exec('from plugins.%s import %s' % (plugin, plugin))
            loaded_plugins.append(plugin)
        except ImportError:
            logger.warning("Cannot load plugin `%s`, ignoring it." % plugin)
    return loaded_plugins

def reload_all_plugins(plugins):
    reloaded_plugins = []
    for plugin in plugins:
        try:
            exec('reload(%s)' % plugin)
            reloaded_plugins.append(plugin)
        except ImportError:
            logger.warning("Cannot reload plugin `%s`, ignoring it." % plugin)
    return reloaded_plugins

if __name__ == '__main__':
    print(load_plugins('./plugins/'))
    print(echo)
