#-*- coding: UTF-8 -*-

import csv
from aiopstools.association_analysis import alarm_association

# 需要分析的监控项
items = ['cpu.idle', 'net.if.totoal.bits.sum', 'mem.memused.percent', 'mem.swapused.percent', 'ss.closed']

if __name__=='__main__':
    # 对于报警特征进行事件与时间序列的相关性检验：此处我们只进行"host.alive"报警的检验，其他类似
    for featurename in items:
        # filename1前5分钟的数据, filename2全时间序列
        filename1 = './aiopstools/association_analysis/data/alarm_association/'+featurename+'/'+'item_alarm_data.csv'
        filename2 = './aiopstools/association_analysis/data/alarm_association/' + featurename +'/'+ 'alldata.csv'
        filename3 ='./aiopstools/association_analysis/data/alarm_association/host.alive.csv'
        csv_file2 = csv.reader(open(filename3, 'r'))
        for row in csv_file2:
            alarmtime = row[1:]
        alarmtime.sort()
        for i in range(len(alarmtime)):
            alarmtime[i] = int(alarmtime[i])

        timeseries_set = []
        csv_file2 = csv.reader(open(filename1, 'r'))
        for row in csv_file2:
            for i in range(len(row)):
                row[i] = float(row[i])
            timeseries_set.append(row)
        timeseries = []
        csv_file2 = csv.reader(open(filename2, 'r'))
        for row in csv_file2:
            for i in range(len(row)):
                timeseries.append(float(row[i]))

        # 生成混合集
        mixset, alarm_number, random_number = alarm_association.mixdata(alarmtime, timeseries_set, timeseries)

        flag = alarm_association.feature_screen(mixset, alarm_number, random_number)
        if flag:
            print(featurename+" is related to alarm")
        else:
            print(featurename + " is not related to alarm")

