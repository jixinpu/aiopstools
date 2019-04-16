#-*- coding: UTF-8 -*-

from __future__ import division
import random
import math
from operator import itemgetter


def mixdata(alarmtime, timeseries_set, timeseries):
    """
    :param alarmtime: 报警的时刻序列,已经排好顺序
    :param timeseries_set: 每个报警时刻的时间序列构成的时序集
    :param timeseries: 报警时刻整体区间内的时序数据
    :return:mixset是混合集，alarm_number报警样本个数，random_number随机样本个数
    """
    mixset = []
    alarm_number = 0
    random_number = 0
    timegap = int((alarmtime[-1]-alarmtime[0]) / 600)
    randomnum = min(len(alarmtime), int(3*timegap/4)) - 1
    for i in range(len(alarmtime)):
        data = timeseries_set[i]
        data.append('alarm')
        if len(data) > 1 and data not in mixset:
            mixset.append(data)
            alarm_number += 1
    while randomnum > 0:
        end = random.randint(5, len(timeseries))
        start = end - 5
        data = timeseries[start:end]
        data.append("random")
        randomnum -= 1
        if len(data) > 1 and data not in mixset:
            mixset.append(data)
            random_number += 1
    return mixset, alarm_number, random_number


def distance(data1,data2):
    dis = 0
    for i in range(0, len(data1)-1):
        dis += (data1[i]-data2[i]) ** 2
    dis = math.sqrt(dis)
    return dis

def feature_screen(mixset, alarm_number, random_number):
    """
    :param mixset: 报警序列与随机序列的混合集
    :param alarm_number: 报警序列个数
    :param random_number: 随机序列个数
    :return: 监控项与报警是否相关
    """
    if alarm_number == 0 or random_number == 0:
        return False
    sum_number = alarm_number + random_number
    mean = (alarm_number/sum_number) ** 2 + (random_number/sum_number) ** 2
    stdDev = (alarm_number/sum_number) * (random_number/sum_number) * (1 + 4 * (random_number/sum_number) * (alarm_number / sum_number))
    R = 10
    trp = 0
    alapha = 1.96
    for j in range(len(mixset)):
        tempdic = {}
        for k in range(len(mixset)):
            if j == k:
                continue
            dis = distance(mixset[j], mixset[k])
            tempdic.setdefault(k, dis)
        temp_list = sorted(tempdic.items(), key=itemgetter(1), reverse=False)[0:R]
        for k in temp_list:
            if mixset[j][-1] == mixset[k[0]][-1]:
                trp += 1

    trp = float(trp / (R*sum_number))
    check = (abs(trp-mean) / stdDev) * math.sqrt(R*sum_number)
    if check > alapha:
        return True
    return False


def get_GR(alarmseries,nomalseries):
    '''
    :param alarmseries: 单一报警的时间序列
    :param nomalseries: 整体报警的时间序列
    :return:
    '''
    cutnum = 10  # 切分份数
    maxvalue = float("-inf")
    minvalue = float("inf")
    GR = 0
    while None in alarmseries:
        alarmseries.remove(None)
    C1 = len(alarmseries)
    if max(alarmseries) > maxvalue:
        maxvalue = max(alarmseries)
    if min(alarmseries) < minvalue:
        minvalue = min(alarmseries)
    while None in nomalseries:
        nomalseries.remove(None)
    C2 = len(nomalseries)
    if max(nomalseries) > maxvalue:
        maxvalue = max(nomalseries)
    if min(nomalseries) < minvalue:
        minvalue = min(nomalseries)
    value_gap = (maxvalue-minvalue) / cutnum
    print(C1)
    print(C2)
    if C1 == 0 or C2 == 0 or value_gap == 0:
        return GR
    HD = (C1 / (C1+C2)) * math.log((C1 / (C1+C2)), 2) + (C2 / (C1+C2)) * math.log((C2 / (C1+C2)), 2)
    Neg = [0] * (cutnum+1)
    Pos = [0] * (cutnum+1)
    for value in alarmseries:
        temp_count = int((value-minvalue) / value_gap) + 1
        if temp_count > cutnum:
            temp_count = cutnum
        Neg[temp_count] += 1
    for value in nomalseries:
        temp_count = int((value-minvalue) / value_gap) + 1
        if temp_count > cutnum:
            temp_count = cutnum
        Pos[temp_count] += 1
    HDA = 0
    HAD = 0
    for j in range(1, cutnum + 1):
        temp = 0
        if Neg[j] != 0 and Pos[j] != 0:
            HAD += ((Neg[j]+Pos[j]) / (C1+C2)) * math.log(((Neg[j]+Pos[j]) / (C1+C2)), 2)
            temp = (Neg[j] / (Neg[j]+Pos[j])) * math.log((Neg[j] / (Neg[j]+Pos[j])), 2) + (Pos[j] / (Neg[j]+Pos[j])) * math.log((Pos[j] / (Neg[j]+Pos[j])), 2)
        elif Neg[j] == 0 and Pos[j] != 0:
            HAD += ((Neg[j]+Pos[j]) / (C1+C2)) * math.log(((Neg[j]+Pos[j]) / (C1 + C2)), 2)
        elif Pos[j] == 0 and Neg[j] != 0:
            HAD += ((Neg[j]+Pos[j]) / (C1+C2)) * math.log(((Neg[j]+Pos[j]) / (C1+C2)), 2)
        HDA += ((Neg[j]+Pos[j]) / (C1+C2)) * temp
    GR = (HD - HDA) / HAD
    return GR