#!/usr/bin/env python3
# -*- coding:utf-8 -*-⏎

from __future__ import print_function
import sys
from urllib import request as urlreq
import urllib.parse


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if sys.version_info<(3,0,0):
    reload(sys)
    sys.setdefaultencoding('utf8')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def read_url(url, retry=1, encoding="utf-8"):
    if not url: return False

    for _ in range(0,retry):
        try:
            c = urlreq.urlopen(url)
            content = c.read()
            if encoding != None:
                content = content.decode(encoding)
            return content

        except Exception as e:
            print(e)
            print(url)
            continue

    return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def urlenc(q):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
    return urllib.parse.quote_plus(q)

