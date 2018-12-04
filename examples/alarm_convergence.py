#-*- encoding: utf-8 -*-

from argparse import ArgumentParser

from aiopstools.association_analysis.apriori import *

def get_data(filename):
    alarm_data = []
    for line in open(filename):
        alarm_sample = []
        line = line.split('\n')
        tmp = line[0].split(' ')
        for i in range(len(tmp)):
            if tmp[i] != '':
                alarm_sample.append(tmp[i])
        if len(alarm_sample) != 0:
            alarm_data.append(alarm_sample)

    return alarm_data


if __name__ == "__main__":
    parser = ArgumentParser(description='Alarm convergence')

    parser.add_argument(
        '--data_dir', default='./aiopstools/association_analysis/data/alarm.txt',
        help='dir of the data')
    # 最小支持度用于生成频繁项集
    parser.add_argument(
        '--minsupport', default=0.2,
        help='mini support')
    # 最小可信度用于生成关联规则
    parser.add_argument(
        '--minconf', default=0.5,
        help='mini conf')

    args = parser.parse_args()

    alarm_data = get_data(args.data_dir)
    L, suppdata = apriori(alarm_data, minSupport=args.minsupport)
    #print(L, suppdata)
    rules = generateRules(L, suppdata, minConf=args.minconf)
    #print(rules)