# -*- encoding: utf-8 -*-

from __future__ import print_function

import os
import pandas as pd
import numpy as np
from argparse import ArgumentParser
from statsmodels.tsa.seasonal import seasonal_decompose

from aiopstools.timeseries_predict import models
from aiopstools.timeseries_predict import handle_data
from aiopstools.timeseries_predict import period_check
from aiopstools.timeseries_predict import accuracy
from aiopstools.timeseries_predict import result_show

def period_predict(decomposition, args, interval):
    """具有周期性时间序列的预测"""
    trend = decomposition.trend
    seasonal = decomposition.seasonal

    trend.dropna(inplace=True)

    model = models.create(args.model_name, predict_time=args.predict_time)

    train_model = model.train(trend, trend.index.time, trend.values)
    predict_data = []
    if train_model is not None:
        predict_data = model.predict(train_model, trend.values)

    # 预测新数据
    interval = str(interval/60) + 'min'
    # 生成长度为n的时间索引，赋给预测序列
    predict_time_index = pd.date_range(start=trend.index[-1], periods=(args.predict_time+1), freq=interval)[1:]

    # 为预测出的趋势数据添加周期数据和残差数据
    values = []

    # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列,同时列出数据和数据下标,一般用在for循环当中。
    for i, t in enumerate(predict_time_index):
        trend_part = predict_data[i]
        # 相同时间点的周期数据均值
        # t为2018-08-09 15:18:00类型的时间,t.time()为15:18:00类型的时间
        season_part = seasonal[seasonal.index.time == t.time()].mean()

        # 趋势 + 周期
        predict = trend_part + season_part

        values.append(round(predict, 2))

    # 得到预测值
    final_predict = pd.Series(values, index=predict_time_index, name='predict')
    return final_predict

def predict_model(timestamp, value, args):
    """预测主函数"""
    dta = handle_data.data_to_datetimeindex(timestamp, value)

    # 历史数据的间隔
    interval = timestamp[1] - timestamp[0]

    if len(dta) > 2*args.predict_time and len(dta[np.isnan(dta)]) != len(dta):
        # 平滑处理
        smooth_data = handle_data.diff_smooth(dta, interval)

        # 周期性检测
        # 具有周期性
        period_result = period_check.period_check(dta, interval)
        print('The result of period is %s' %period_result)

        if period_result == 'yes':
            try:
                # 周期性分解
                decomposition = seasonal_decompose(smooth_data, two_sided=False)
            except:
                print('The freq of series is not supported.')
                return

            # 用treand部分进行预测
            result = period_predict(decomposition, args, interval)
            if result is not None:
                return result.values
            else:
                print('The result of prediction os None')
                return

        # 不具有周期性
        else:
            model = models.create(args.model_name, predict_time=args.predict_time)

            train_model = model.train(smooth_data, smooth_data.index.time, smooth_data.values)
            predict_data = []
            if train_model is not None:
                predict_data = model.predict(train_model, smooth_data.values)
            else:
                print('The result of prediction os None')
                return
            return predict_data


def check_param(args):
    """检测命令行参数的合法性"""
    # 所有支持的模型
    model_list = ['lr', 'ann', 'lstm', 'arima']

    if args.model_name not in model_list:
        return 'unknown model'
    # 预测时间必须是整数，且不等于0
    if not isinstance(args.predict_time, int) and args.predict_time == 0:
        return 'error predict time'
    if not os.path.exists(args.data_dir):
        return 'the data file is not exist'
    else:
        return ''

if __name__ == "__main__":
    parser = ArgumentParser(description='Periodic prediction of the time series.')

    parser.add_argument(
        '--model_name', default='lr',
        choices=models.names(), help='Name of the model to use.')

    parser.add_argument(
        '--data_dir', default='./aiopstools/timeseries_predict/data/timeseries_data.csv',
        help='Dir of the data to train')

    parser.add_argument(
        '--predict_time', type=int,
        help='The prediction time.')

    args = parser.parse_args()

    check_result = check_param(args)
    if check_result == '':
        ori_data, timestamp_list, value_list = handle_data.get_train_data(args.data_dir, args.predict_time)
        predict_data = predict_model(timestamp_list, value_list, args)
        print("the prediction result:")
        print(predict_data)
        truth_data = handle_data.get_truth_data(args.data_dir, args.predict_time)
        if predict_data is not None and truth_data is not None:
            accuracy = accuracy.pct(predict_data, truth_data)
            print("the prediction error:%f" %accuracy)
            #get_figure(value_list, predict_data, truth_data)
        else:
            print('The result of prediction is null')
    else:
        print(check_result)
