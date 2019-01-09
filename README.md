# aiopstools
aiopstools是aiops领域公开的工具包，里面提供的功能包括：
- 时间序列的预测；
- 异常检测；
- 关联分析；

## 环境

```
cd aiopstools
python setup.py install
```

## 时间序列异常检测
时间序列异常检测机制是对单变量时间序列的异常情况进行检测。该检测机制有以下优点：
- 克服了负样本少的问题，采用无监督算法；
- 单个算法误报多的问题，采用多种算法投票来减少误报率；
- 特征提取：参考统计特征（同比、环比、振幅）、拟合特征；

在真实的数据集上，我们的检测算法的准确率能达到95%以上，效果还是不错的。

### 运行
#### 数据
该检测机制检测的是时间序列，当然需要的数据也是时间序列，你可以使用我们例子的数据，当然也可以使用自己的数据，但需要将数据整理成
./aiopstools/anomaly_detection/data/data.csv格式。

#### 例子
我们用一个数据集来说明如何对序列进行检测，该例子使用的数据./aiopstools/anomaly_detection/data/data.csv。该数据中，我们将最后一个点作为检测点，其
其他的数据作为训练数据。

```
python examples/detection.py --data_dir=./aiopstools/anomaly_detection/data/data.csv --period_freq='D' --voting_num=3
```

该脚本中的几个参数：
- data_dir：数据集的目录
- period_freq: 序列的周期，支持H(小时)、D(天)、M(月)和Y(年)
- voting_num：参与投票的算法符合的个数，建议为3

**具体的检测算法参考docs/anomaly_detection.md**

## 报警收敛

该模块可以分析出A->B这样的关联规则，这样在一定的时间窗口内，如果A和B同时发生，就可以只发A报警，而不发B报警，这样就可以减少报警的次数。

以机器为维度，一定的时间窗口内，分析不同监控项的关联情况。使用Apriori算法进行关联分析。

### 使用
minsupport为最小支持度，用于生成符合条件的频繁项集，minconf为最小支持度，用于生成关联规则。
```
python examples/alarm_convergence.py --data_dir=./aiopstools/association_analysis/data/alarm.txt --minsupport=0.2 --minconf=0.5
```

## 时间序列预测

本项目用作单变量的时间序列的预测，目前支持的模型有lr、arima、bp神经网络和lstm。

### 运行
本项目提供两种运行方式，一种是非周期性预测，一种是周期性预测。

所谓非周期性就是不进行周期性检测，直接进行预测；而周期性预测是先进行周期性检测，之后根据周期性的情况选择预测模型。下面是周期性预测的流程图，非周期性预测去掉周期性检测，剩下的部分一样。

![img](https://ws1.sinaimg.cn/large/006tNbRwly1fx6k2ynpz7j30jo0aj74n.jpg)

我们提供两种运行方式，

#### 非周期性预测

##### 数据

将数据文件data.csv放在如./aiopstools/timeseries_predict/data中。格式如下：

```
timestamp,value
0,1.0
1,2.0
……
```

timestamp可以为0，1，2这样的格式，也可以是“1540796400”这种时间戳。

##### 预测

```
python examples/timeseries_predict.py --model_name=ann --data_dir='./aiops/timeseries_predict/data/data.csv' --predict_time=24
```

**详细的结果文档见docs/predict_result.md**

#### 周期性预测

##### 数据

将数据文件timeseries_data.csv放在如./aiops/timeseries_predict/data中。格式如下：

```
timestamp,value
1540796400,1.0
1540800000,2.0
……
```

timestamp必须是“1540796400”这种时间戳。

##### 预测

```
python examples/timeseries_period_predict.py --model_name=lr --data_dir='.aiopstools/timeseries_predict/data/timeseries_data.csv' --predict_time=24
```

**详细结果的文档见docs/predict_result.md**

另外，周期性预测中有个**周期性检测**的方法，具体的检测流程见**docs/period_check.md**。

### 结果

这四个模型的时间开销和准确率如下：

|               模型                |   时间开销    | 准确率 |                 开源包                 |
| :-------------------------------: | :-----------: | :----: | :------------------------------------: |
|          LR（线性回归）           |      少       |   低   |                 skearn                 |
|               ARIMA               |      少       |   低   |              statsmodels               |
| 浅层神经网络(迭代100次)、回归树等 |     中等      |   中   | 浅层神经网络(pybrain)、回归树(sklearn) |
|               LSTM                | 大（需要GPU） |   高   |               tensorflow               |

### 建议

如果你的数据是如data.csv这样的不带时间戳格式，你可以选择非周期性预测，模型可以根据需要选择上面四种的一种；而如果你的数据如timeseries_data.csv这样带时间戳的格式，建议你选择周期性预测，这样即使选择LR这种精度不太高的模型也可以达到比较好的效果。

你可能有这样的疑问：doc/predict_result.md里面使用的时序数据具有周期性，那如果没有周期性趋势的数据使用周期性预测是不是效果不好？

结果不是这样的，因为我们在周期性预测的时候，首先去判断该序列是否具有周期性，如果具有周期性的话，才会去提取趋势特征，如果没有周期性，我们将使用原来的数据进行预测。

### 交流
如果对aiops感兴趣，可以和我进行交流，我的邮箱：

jixinpu@126.com

除此之外，我还建立了aiops的知乎专栏，上面会经常更新一些aiops的最新研究进展，知乎专栏地址：

https://zhuanlan.zhihu.com/c_178702079

