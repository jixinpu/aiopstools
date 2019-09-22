#-*- coding: UTF-8 -*-

import datetime
import numpy as np

class POP(object):
    """同比最值(最大值和最小值)"""
    def __init__(self, freq):
        self.min_threshold = 1
        self.max_threshold = 0.8
        self.freq = freq

    def get_pop_data(self, data):
        data_list = []
        # 同比检测的次数
        check_num = 7
        try:
            start_index = data.index[-1]
            data_list.append(data.values[-1])
            for i in range(check_num-1):
                a_index = ''
                if self.freq == 'H':
                    a_index = start_index + datetime.timedelta(minutes=int(-60))
                elif self.freq == 'D':
                    a_index = start_index + datetime.timedelta(hours=int(-24))
                elif self.freq == 'M':
                    a_index = start_index + datetime.timedelta(days=int(-30))
                elif self.freq == 'Y':
                    a_index = start_index + datetime.timedelta(months=int(-12))
                else:
                    print('The freq is not supported.')
                    return
                start_index = a_index
                if a_index not in data.index:
                    print('less data')
                else:
                    data_list.append(data[a_index])
        except:
            print('error occurred during getting data')
            return

        return data_list

    def check(self, data, check_value):
        """计算数据的同比,data是列表形式"""
        pop_data = self.get_pop_data(data)
        # 记录同比率
        pop_percent = []
        if len(pop_data) > 0:
            for i in range(len(pop_data)):
                pre = 0.0
                if pop_data[i] != 0.0:
                    pre = abs((check_value - pop_data[i])/pop_data[i])
                else:
                    pre = abs((check_value - pop_data[i])/(1+pop_data[i]))
                pop_percent.append(pre)

            value = np.mean(pop_percent)
            simultaneous_data_max = max(pop_data)
            simultaneous_data_min = min(pop_data)
            if simultaneous_data_min * self.min_threshold >= check_value and (check_value - data.values[-1]) < 0:
                return "anticlimax", value
            if data[-1] > simultaneous_data_max * self.max_threshold and (check_value - data.values[-1]) > 0:
                return "uprush", value
            else:
                return "no alarm", value
        else:
            print('The num of pop data is little.')

class POP_Amplitude(object):
    """同比振幅"""
    def __init__(self, freq):
        self.min_threshold = 0.5
        self.max_threshold = 0.5
        self.freq = freq

    def get_amplitude_data(self, data, check_value):
        amplitude_data_list = []
        # 同比振幅检测的次数
        check_num = 7
        try:
            start_index = data.index[-1]
            start = data.values[-1]
            last_amplitude = 0.0
            if start != 0.0:
                last_amplitude = (check_value - start) / start
            else:
                last_amplitude = (check_value - start) / (1 + start)
            amplitude_data_list.append(last_amplitude)
            for i in range(check_num-1):
                a_index = ''
                if self.freq == 'H':
                    a_index = start_index + datetime.timedelta(minutes=int(-60))
                elif self.freq == 'D':
                    a_index = start_index + datetime.timedelta(hours=int(-24))
                elif self.freq == 'M':
                    a_index = start_index + datetime.timedelta(days=int(-30))
                elif self.freq == 'Y':
                    a_index = start_index + datetime.timedelta(months=int(-12))
                else:
                    print('The freq is not supported.')
                    return
                start_index = a_index
                if a_index not in data.index:
                    print('less data')
                else:
                    index_list = data.index.tolist()
                    end_index = index_list.index(a_index)
                    x = data[start_index]
                    y = data.values[end_index]
                    
                    if x != 0.0:
                        tmp = (y - x) / x
                        if tmp == 0.0:
                            tmp = tmp + 0.1
                        amplitude_data_list.append(abs(round(tmp, 2)))
                    else:
                        tmp = (y - x) / (x + 1)
                        if tmp == 0.0:
                            tmp = tmp + 0.1
                        amplitude_data_list.append(abs(round(tmp, 2)))

        except:
            print('error occurred during getting data')
            return

        return amplitude_data_list

    def check(self, data, check_value):
        """振幅的最大值"""
        # 归一化
        #maxvalue = np.max(data)
        #minvalue = np.min(data)
        #for i in range(len(data)):
        #    data[i] = (data[i]-minvalue)/(maxvalue-minvalue)

        amplitude_data = self.get_amplitude_data(data, check_value)
        if len(amplitude_data) >= 1:
            value = np.mean(amplitude_data)
            if abs(amplitude_data[0]) > np.max(amplitude_data) * self.max_threshold and check_value > data.values[-1]:
                return "uprush", value
            if abs(amplitude_data[0]) > np.max(amplitude_data) * self.min_threshold and check_value < data.values[-1]:
                return "anticlimax", value
            else:
                return "no alarm", value

class Tail(object):
    """环比(相邻节点)"""
    def __init__(self, freq):
        self.threshold = 0.3
        self.tail_num = 10
        self.freq = freq

    def check(self, timeseries, check_value):
        """
        计算数据的环比
        比较检测点和最近n个值的差值。
        """
        data = timeseries.values
        # 计算动态阈值
        max_avg = np.max(data) - np.mean(data)
        min_avg = np.mean(data) - np.min(data)
        threshold = min(max_avg, min_avg)*self.threshold

        # 环比数据
        tail_data = []
        # 环比变化率
        tail_percent = []
        end = data[-1]
        for i in range(1, self.tail_num):
            # 计算差值
            start = data[-i-1]
            tail_data.append(abs(start - check_value))
            # 计算变化率
            percent = 0.0
            if start != 0:
                percent = abs((start - check_value)/start)
            else:
                percent = abs((start - check_value)/(1 + start))
            tail_percent.append(percent)
        value = np.mean(tail_percent)

        # 环比类型(最后一个值和倒数第二个值的关系)
        last_type = check_value - data[-2]
        # 差值超过阈值的次数
        count = 0
        for i in range(len(tail_data)):
            if tail_data[i] > threshold:
                count = count + 1
        if count > 0 and last_type > 0:
            return "uprush", value
        if count > 0 and last_type < 0:
            return "anticlimax", value
        else:
            return "no alarm", value
