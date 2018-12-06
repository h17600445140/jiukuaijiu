#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib

def md(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()
