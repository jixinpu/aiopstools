#-*- coding: UTF-8 -*-

import numpy as np
from sklearn.ensemble import IsolationForest

class IForest(object):
    def __init__(self, freq):
        self.threshold = 0.01
        self.freq = freq

    def check(self, timeseries_data, check_value):
        data = timeseries_data.values.tolist()
        check_value_list = []
        check_value_list.append([check_value])
        # 孤立森林异常点检查，data是列表形式
        x_train = []
        for i in range(len(data)):
            x_train.append([data[i]])
        clf = IsolationForest(behaviour='new', max_samples=100)
        clf.fit(x_train)
        scores_pred = clf.predict(check_value_list)
        if scores_pred[-1] < 0:
            if check_value > data[-1]:
                return "uprush", scores_pred[-1]
            else:
                return "anticlimax", scores_pred[-1]
        else:
            return "no alarm", 0