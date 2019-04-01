报警关联分析模块是参考微软2014年SIGKDD会议上发表的论文《Correlating Events with Time Series for Incident Diagnosis》，我们将论文提出的方法进行实现。

## 数据

分析报警项和监控项之间的关系，需要知道报警发生时刻，监控项的时间序列。有了监控项的时间序列，我们就可以得到报警发生前后，监控项的数据。有了这些数据，就可以使用论文中的方法。

## 运行

结合一个简单的demo来说明如何使用该模块。我们用到的报警项和监控项如下表格：

|          项           |       中文       |  功能  |
| :-------------------: | :--------------: | :----: |
|      host.alive       |     存活监控     | 报警项 |
|       cpu.idle        |    cpu空闲率     | 监控项 |
| mem.swapused.percent  |    swap使用率    | 监控项 |
|  mem.memused.percent  |    内存使用率    | 监控项 |
| net.if.total.bits.sum |     网卡流量     | 监控项 |
|       ss.closed       | closed状态连接数 | 监控项 |

host.alive是我们的报警项，cpu.idle、mem.swapused.percent、mem.memused.percent、net.if.total.bits.sum以及ss.closed是我们的监控项，我们需要分析哪些监控项跟host.alive报警项有关。

报警项需要的数据是报警发生的时刻，整理成[报警发生时刻数据](https://github.com/jixinpu/aiopstools/tree/master/aiopstools/association_analysis/data/alarm_association/host.alive.csv)

监控项需要两个数据，一个是监控项的时间序列数据（nodedata.csv），一个是报警时刻之前的5分钟数据（item_alarm_data.csv）

有了这些数据以后，就可以运行下面的命令：

```
python examples/alarm_association.py
```

结果会进行打印，就可以找出哪些监控项跟报警相关。

## 结果
我们对上面的方法进行了测试，使用6个事件和100+个监控项，取报警事件最相关的top5指标，效果如下表：

![image-20181024175406044](https://ws4.sinaimg.cn/large/006tNbRwly1fwjgoi8teij30l50legpn.jpg)

可以看到平均准确率能够达到85%，效果还是不错的。
