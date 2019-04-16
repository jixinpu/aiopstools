#-*- coding: UTF-8 -*-

from pandas import DataFrame

class Ewma(object):
    def __init__(self, freq):
        self.com = 20
        self.freq = freq

    def check(self, data, check_value):
        """指数加权移动平均模型
        衡量序列的整体水平，方便检测出短期趋势
        """
        df = DataFrame({'data':data})
        expAverage = df.ewm(com=20).mean()
        stdDev = df.ewm(com=20).std()

        # 检测点和整个序列的均值和标准差进行比较
        if abs(check_value - expAverage['data'][len(expAverage['data'])-1]) > 3*stdDev['data'][len(expAverage['data'])-1] and (check_value-data[-1])> 0:
            return "uprush", abs(check_value-expAverage['data'][len(expAverage['data'])-1])
        if abs(check_value - expAverage['data'][len(expAverage['data'])-1]) > 3*stdDev['data'][len(expAverage['data'])-1] and (check_value-data[-1])< 0:
            return "anticlimax", abs(check_value-expAverage['data'][len(expAverage['data'])-1])
        else:
            return "no alarm", abs(check_value-expAverage['data'][len(expAverage['data'])-1])
