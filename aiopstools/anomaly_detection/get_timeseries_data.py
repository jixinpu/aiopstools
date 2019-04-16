#-*- encoding: utf-8 -*-

import time
import pandas as pd

def get_data(filename):
    """从csv中获取数据
    :param filename:文件名
    :return:
    dta:series格式的时间序列
    check_value:需要检测的值
    """
    data = pd.read_csv(filename)
    timestamp_list = []
    value_list = []
    for timestamp, value in zip(data['timestamp'], data['value']):
        a = time.localtime(timestamp)
        b = time.strftime("%Y-%m-%d %H:%M:%S", a)
        timestamp_list.append(b)
        value_list.append(value)
    dta = pd.Series(value_list[:-1])
    dta = dta.fillna(dta.mean())
    dta.index = pd.Index(timestamp_list[:-1])
    dta.index = pd.DatetimeIndex(dta.index)
    # 最后一个点为检测点
    check_value = value_list[-1]
    return dta, check_value