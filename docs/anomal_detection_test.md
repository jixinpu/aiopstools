时间序列异常检测机制是对单变量时间序列的异常情况进行检测。该检测机制有以下优点：

- 克服了负样本少的问题，采用无监督算法；
- 单个算法误报多的问题，采用多种算法投票来减少误报率；
- 特征提取：参考统计特征（同比、环比、振幅）、拟合特征；

在真实的数据集上，我们的检测算法的准确率能达到95%以上，效果还是不错的。

# 运行

## 数据

该检测机制检测的是时间序列，当然需要的数据也是时间序列，你可以使用我们例子的数据，当然也可以使用自己的数据，但需要将数据整理成
./aiopstools/anomaly_detection/data/data.csv格式。

## 例子

我们用一个数据集来说明如何对序列进行检测，该例子使用的数据./aiopstools/anomaly_detection/data/data.csv。该数据中，我们将最后一个点作为检测点，其
其他的数据作为训练数据。

```
python examples/detection.py --data_dir=./aiopstools/anomaly_detection/data/data.csv --period_freq='D' --voting_num=3
```

该脚本中的几个参数：

- data_dir：数据集的目录
- period_freq: 序列的周期，支持H(小时)、D(天)、M(月)和Y(年)
- voting_num：参与投票的算法符合的个数，建议为3

**具体的检测算法参考[异常检测](https://github.com/jixinpu/aiopstools/blob/master/docs/anomal_detection.md)**