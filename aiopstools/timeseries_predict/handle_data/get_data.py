#-*- encoding: utf-8 -*-

import pandas as pd
from aiopstools.timeseries_predict.handle_data.process import *

def get_train_data(data_dir, predict_time):
    """从csv文件中获取训练数据
    返回：
    dta: Series类型，时间序列
    timestamp_list: 时间戳列表
    value_list: 数据列表
    """
    filename = data_dir
    data = pd.read_csv(filename)
    timestamp_list = []
    value_list = []
    # data中去掉后面predict_time数据，作为验证部分
    data = data[:-int(predict_time)]
    for timestamp, value in zip(data['timestamp'],data['value']):
        timestamp_list.append(timestamp)
        value_list.append(value)

    dta = data_to_datetimeindex(timestamp_list, value_list)
    return dta, timestamp_list, value_list

def get_truth_data(data_dir, predict_time):
    """从csv文件中获取预测真实数据
        返回：
        dta: Series类型，时间序列
        timestamp_list: 时间戳列表
        value_list: 数据列表
        """
    filename = data_dir
    data = pd.read_csv(filename)
    value_list = []
    # data中只保留后面predict_time数据，作为验证
    data = data[-int(predict_time):]
    for _, value in zip(data['timestamp'], data['value']):
        value_list.append(value)

    return value_list
