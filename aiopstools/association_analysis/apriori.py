# -*- encoding: utf-8 -*-

import sys
from numpy import *

def createC1(dataSet):
    """生成大小为1的候选项集"""
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    # 使用frozenset
    return list(map(frozenset, C1))


def scanD(D, Ck, minSupport):
    """选出大于最小支持度的项集

    参数：
    D: set类型
    Ck: 候选集列表
    minSupport: 最小支持度

    返回:
    retList, supportData
    """
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        # 计算所有项集的支持度
        support = ssCnt[key]/numItems
        # support = ssCnt[key]
        # 保留支持度大于最小支持度
        if float(support) >= float(minSupport):
            # 插入到列表0号位置
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k):
    """构建候选集Ck
    如以{0}、{1}、{2}作为输入，会生成{0,1}、{0,2}、{1,2}

    参数：
    Lk:频繁项集列表
    k:项集元素的个数

    返回:
    Ck
    """
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2];
            L2 = list(Lk[j])[:k - 2]
            L1.sort();
            L2.sort()
            # 前k-2个项相同时，将两个集合合并
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def apriori(dataSet, minSupport):
    """使用Apriori算法来发现频繁项集

    参数：
    dataSet: 数据集
    minSupport: 最小支持度

    返回:
    L:满足最小支持度的频繁项集列表
    supportData:所有项集的支持度
    """
    # 生成候选集列表
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))
    # 得到L1
    L1, supportData = scanD(D, C1, minSupport)
    # L为频繁项集，L最后包含L1，L2，L3...
    L = [L1]
    k = 2
    # 继续寻找L2，L3...
    while (len(L[k - 2]) > 0):
        # 构建候选集
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(L, supportData, minConf=0.7):
    """关联规则生成函数:从频繁项集中挖掘关联规则"""
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    """计算可信度函数"""
    prunedH = []
    for conseq in H:
        # 计算可信度
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if float(conf) >= float(minConf):
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet - conseq, conseq, round(conf, 2)))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
