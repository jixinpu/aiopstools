该模块可以分析出A->B这样的关联规则，这样在一定的时间窗口内，如果A和B同时发生，就可以只发A报警，而不发B报警，这样就可以减少报警的次数。

以机器为维度，一定的时间窗口内，分析不同监控项的关联情况。使用Apriori算法进行关联分析。

# 使用

minsupport为最小支持度，用于生成符合条件的频繁项集，minconf为最小支持度，用于生成关联规则。

```
python examples/alarm_convergence.py --data_dir=./aiopstools/association_analysis/data/alarm.txt --minsupport=0.2 --minconf=0.5
```

