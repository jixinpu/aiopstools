# 简介
报警收敛

以机器为维度，一定的时间窗口内，分析不同监控项的关联情况。

使用Apriori算法进行关联分析。

# 使用
minsupport为最小支持度，用于生成符合条件的频繁项集，minconf为最小支持度，用于生成关联规则。
```
python alarm_convergence.py --data_dir=./association_analysis/data/alarm.txt --minsupport=0.2 --minconf=0.5
```