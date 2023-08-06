#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = 'dict_'
__author__ = 'JieYuan'
__mtime__ = '18-12-14'
"""

from xplan import X
import json


@X
def xjson(dict_):
    _ = json.dumps(dict_, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
    return _




if __name__ == '__main__':
    print({'a': 1} | xjson)