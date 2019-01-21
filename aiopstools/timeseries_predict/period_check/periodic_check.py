#-*- encoding: utf-8 -*-

import numpy as np
from dtw import dtw
from aiopstools.timeseries_predict.handle_data.process import diff_smooth


def period_check(timeseries, interval):
    """周期性检测算法"""
    # 检测结果
    check_result = ''
    # DTW参数
    dtw_threshold = 3
    # 保证timeseries不全为nan
    if len(timeseries[np.isnan(timeseries)]) != len(timeseries):
        # 平滑处理
        smooth_data = diff_smooth(timeseries, interval)
        # 分段
        split_data = np.array(smooth_data).reshape(-1, 24)
        # 求相邻段之间的DTW距离
        dist_list = []
        for j in range(len(split_data)-1):
            x = np.array(split_data[j]).reshape(-1, 1)
            y = np.array(split_data[j+1]).reshape(-1, 1)

            dist, cost, acc, path = dtw(x, y, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
            dist_list.append(dist)

        if len(dist_list) > 0:
            max_value = np.max(smooth_data)
            min_value = np.min(smooth_data)
            if np.max(dist_list) > dtw_threshold:
                check_result = 'no'
            else:
                if (max_value - min_value) > dtw_threshold:
                    check_result = 'no'
                else:
                    check_result = 'yes'
        else:
            print('DTW is null')
            check_result = 'no'
    else:
        print('The elements of timeseries are all nan')
        check_result = 'no'

    return check_result
