#-*- encoding: utf-8 -*-

import aiopstools.anomaly_detection.models as models


def voting(data, check_value, freq, voting_num):
    """无监督投票检测机制

    :param data:时间序列
    :param check_value:检测值
    :param freq: 周期值
    :return: 检测结果
    """
    check_result_list = {}
    # 支持的模型
    model_list = ['pop', 'amplitude', 'tail', 'iforest', 'fitting']
    for i in range(len(model_list)):
        print(model_list[i])
        alg = models.create(model_list[i], freq)
        result = alg.check(data, check_value)
        check_result_list[model_list[i]] = result

    result_type_list = []
    for i in check_result_list:
        print("model: %s" %i)
        print("check result:%s, percent:%f" %(check_result_list[i][0], check_result_list[i][1]))
        result_type_list.append(check_result_list[i][0])

    if result_type_list.count('uprush') >= voting_num:
        return 'uprush'
    elif result_type_list.count('anticlimax') >= voting_num:
        return 'anticlimax'
    else:
        return 'no alarm'
