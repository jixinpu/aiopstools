本项目用作单变量的时间序列的预测，目前支持的模型有lr、arima、bp神经网络和lstm。

### 运行

本项目提供两种运行方式，一种是非周期性预测，一种是周期性预测。

所谓非周期性就是不进行周期性检测，直接进行预测；而周期性预测是先进行周期性检测，之后根据周期性的情况选择预测模型。下面是周期性预测的流程图，非周期性预测去掉周期性检测，剩下的部分一样。

![img](https://ws1.sinaimg.cn/large/006tNbRwly1fx6k2ynpz7j30jo0aj74n.jpg)

我们提供两种运行方式，一种是非周期性预测，一种是周期性预测，下面将对这两种方式进行介绍。

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
python examples/ts_predict.py --model_name=ann --data_dir='./aiopstools/timeseries_predict/data/data.csv' --predict_time=24
```

**详细的结果文档见docs/predict_result.md**

#### 周期性预测

##### 数据

将数据文件timeseries_data.csv放在如./aiopstools/timeseries_predict/data中。格式如下：

```
timestamp,value
1540796400,1.0
1540800000,2.0
……
```

timestamp必须是“1540796400”这种时间戳。

##### 预测

```
python examples/ts_period_predict.py --model_name=lr --data_dir='./aiopstools/timeseries_predict/data/timeseries_data.csv' --predict_time=24
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