# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------
# Author:  Bruce Zhang
# Email:   zy183525594@163.com
# Version: 0.1
# -----------------------------

import re
import os
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.edmundson import EdmundsonSummarizer as Summarizer


def summarize(args):
    argus = args.split()
    if len(argus) == 0:
        return 'Summarize usage: summarize <url> (percentage)'
    elif argus[0].lower() == '--help':
        return 'Summarize usage: summarize <url> (percentage)'
    elif len(argus) == 1:
        return _exec_sum(argus[0])
    elif len(argus) == 2:
        return _exec_sum(argus[0], argus[1])
    else:
        return 'too many aruments.'


def _exec_sum(url, pct='15%'):
    sentences = []
    if _is_httplink(url):
        cmd = os.popen('sumy luhn --url=%s --length=%s' % (url, pct))
        return cmd.read()
    return False


def _is_httplink(words):
    return re.match(r'^https?://', words)
