#-*- coding: UTF-8 -*-

import csv
from aiopstools.association_analysis import alarm_association

# 需要分析的监控项
ITEMS = ['cpu.idle', 'net.if.totoal.bits.sum', 'mem.memused.percent', 'mem.swapused.percent', 'ss.closed']

if __name__=='__main__':
    # 对于报警特征进行事件与时间序列的相关性检验：此处我们只进行"host.alive"报警的检验，其他类似
    for item in ITEMS:
        # alarm_filename为报警前5分钟的数据, alldata_filename为全时间序列的数据
        alarm_data_filename = './aiopstools/association_analysis/data/alarm_association/'+item+'/'+'item_alarm_data.csv'
        alldata_filename = './aiopstools/association_analysis/data/alarm_association/' + item +'/'+ 'alldata.csv'
        item_data_filename ='./aiopstools/association_analysis/data/alarm_association/host.alive.csv'

        item_data_csv_file = csv.reader(open(item_data_filename, 'r'))

        for row in item_data_csv_file:
            alarmtime = row[1:]
        alarmtime.sort()
        for i in range(len(alarmtime)):
            alarmtime[i] = int(alarmtime[i])

        timeseries_set = []
        item_data_csv_file = csv.reader(open(alarm_data_filename, 'r'))
        for row in item_data_csv_file:
            for i in range(len(row)):
                row[i] = float(row[i])
            timeseries_set.append(row)
        timeseries = []
        item_data_csv_file = csv.reader(open(alldata_filename, 'r'))
        for row in item_data_csv_file:
            for i in range(len(row)):
                timeseries.append(float(row[i]))

        # 生成混合集
        mixset, alarm_number, random_number = alarm_association.mixdata(alarmtime, timeseries_set, timeseries)

        flag = alarm_association.feature_screen(mixset, alarm_number, random_number)
        if flag:
            print(item + " is related to alarm")
        else:
            print(item + " is not related to alarm")

