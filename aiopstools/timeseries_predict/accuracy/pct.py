#-*- encoding: utf-8 -*-

import numpy as np

def pct(predict_value, truth_value):
    """预测准确度"""
    if len(predict_value) != len(truth_value):
        print('The length of predict_value and truth_value is not same.')
        return

    predict_value = np.array(predict_value)
    truth_value = np.array(truth_value)
    # 求预测值和真实值的差距百分比
    pct_value = np.true_divide(abs(predict_value-truth_value),truth_value)
    # 求所有pct的均值
    pct_mean_value = np.mean(pct_value)
    return pct_mean_value