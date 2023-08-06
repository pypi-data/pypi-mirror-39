#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'iter'
__author__ = 'JieYuan'
__mtime__ = '18-12-14'
"""
from xplan.utils import X

import numpy as np
import pandas as pd
from functools import reduce
from pprint import pprint
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from xplan.eda import DataFrameSummary

try:
    from IPython import get_ipython

    if 'IPKernelApp' not in get_ipython().config:
        raise ImportError("console")
except:
    from tqdm import tqdm

else:
    from tqdm import tqdm_notebook as tqdm

# base types
xtuple, xlist, xset = X(tuple), X(list), X(set)

xseries = X(lambda iterable, name='iterable': pd.Series(iterable, name=name))
xdataframe = X(lambda iterable, name='iterable': pd.DataFrame({name: iterable}))

# 高阶函数
xmap = X(lambda iterable, func: map(func, iterable))
xreduce = X(lambda iterable, func: reduce(func, iterable))
xfilter = X(lambda iterable, func: filter(func, iterable))

# 统计函数: 待补充groupby.agg
xsummary = X(lambda iterable: DataFrameSummary(iterable | xdataframe)['iterable'])
funcs = [sum, min, max, abs, len, np.mean, np.median]
xsum, xmin, xmax, xabs, xlen, xmean, xmedian = [X(i) for i in funcs]

xnorm = X(lambda iterable, ord=2: np.linalg.norm(iterable, ord))
xcount = X(lambda iterable: Counter(iterable))
xcounts = X(lambda iterable, name='iterable': (iterable | xseries(name=name)).value_counts())
xunique = X(lambda iterable: list(OrderedDict.fromkeys(iterable)))  # 移除列表中的重复元素(保持有序)
xsort = X(lambda iterable, reverse=False, key=None: sorted(iterable, key=key, reverse=reverse))

max_index = X(lambda x: max(range(len(x)), key=x.__getitem__))  # 列表中最小和最大值的索引
min_index = X(lambda x: min(range(len(x)), key=x.__getitem__))  # 列表中最小和最大值的索引
most_freq = X(lambda x: max(set(x), key=x.count))  # 查找列表中频率最高的值, key作用于set(x), 可类推出其他用法


# print
xprint = X(pprint)
xtqdm = X(lambda iterable, desc=None: tqdm(iterable, desc))


# multiple
@X
def xmultiple_thread(iterable, func, max_workers=5):
    with ThreadPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


@X
def xmultiple_process(iterable, func, max_workers=5):
    with ProcessPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)
