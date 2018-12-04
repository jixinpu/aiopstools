#-*- encoding: utf-8 -*-

import time
import datetime
import numpy as np
import pandas as pd

def diff_smooth(ts, interval):
    """平滑处理"""
    # interval最小单位为秒，除以60就变为分钟，方便下面处理.
    wide = interval/60
    # 一阶差分
    dif = ts.diff().dropna()
    # 描述性统计得到：min，25%，50%，75%，max值
    td = dif.describe()
    # 定义高点阈值，1.5倍四分位距之外
    high = td['75%'] + 1.5 * (td['75%'] - td['25%'])
    # 定义低点阈值
    low = td['25%'] - 1.5 * (td['75%'] - td['25%'])

    i = 0
    # 变化幅度超过阈值的点的索引
    forbid_index = dif[(dif > high) | (dif < low)].index
    while i < len(forbid_index) - 1:
        n = 1
        # 异常点的起始
        start = forbid_index[i]
        while forbid_index[i+n] == start + datetime.timedelta(minutes=n):
            n += 1
        i += n - 1
        # 异常点的结束
        end = forbid_index[i]
        # np.linspace(start, end, num)生成等差数列
        # 用前后值均匀填充
        value = np.linspace(ts[start - datetime.timedelta(minutes=wide)], ts[end + datetime.timedelta(minutes=wide)], n)
        ts[start: end] = value
        i += 1
    return ts

def data_to_datetimeindex(timestamp, value):
    """将数据变为Series类型"""
    time_list = []
    for i in range(len(timestamp)):
        a = time.localtime(timestamp[i])
        b = time.strftime("%Y-%m-%d %H:%M:%S", a)
        time_list.append(b)

    dta = pd.Series(value)
    dta = dta.fillna(dta.mean())
    dta.index = pd.Index(time_list)
    dta.index = pd.DatetimeIndex(dta.index)
    return dta