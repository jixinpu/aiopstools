# 简介

我们先介绍不用检测周期性，直接进行时间序列预测。

为了比较模型的效果，我们引入一个评价因子PCT来说明每个模型的好坏。所谓的PCT就是

![image-20181112155404387](https://ws1.sinaimg.cn/large/006tNbRwly1fx5bzh48imj3078020a9z.jpg)

接下来我们将结合一个例子，从PCT和时间开销(time)两方面来衡量一下模型。

# 模型效果

我们取线上的一个时间序列，一共有336个值。前312个值作为训练，后24个值作为测试和验证效果。前312个值如下图所示，用肉眼看，该时间序列具有比较强的周期性。我们先后用非周期性预测和周期性预测两种方法来说明效果。

![image-20181112151947357](https://ws1.sinaimg.cn/large/006tNbRwly1fx5azxxnv8j30fq0bwdh4.jpg)

### 非周期性预测

#### LR

首先介绍线性回归，效果如下图。

![image-20181112152655900](https://ws4.sinaimg.cn/large/006tNbRwly1fx5b79zxryj30g40bwwfw.jpg)

可以看到该模型预测结果基本趋于平均值。其中PCT为0.085063，而time为1.27s。

## ARIMA

接下来介绍ARIMA模型，在该算法中，我们在差分为1的情况下，用bic准则取确定p和q的值，效果如下图：

![image-20181112152845546](https://ws2.sinaimg.cn/large/006tNbRwly1fx5b96darwj30fo0bujss.jpg)

跟LR差不多，其中PCT为0.092，time为1.43s。

## bp神经网络

再接着介绍bp神经网络，在该神经网络中，我们使用只有一层的隐藏层，输入层个数为predict_time（预测时间），隐藏层为2*predict_time，输出层为predict_time，学习速率为0.01，迭代100次，结果如下：

![image-20181112153041537](https://ws2.sinaimg.cn/large/006tNbRwly1fx5bb52vxyj30fs0bxdh9.jpg)

结果PCT为0.087210，time为1.56s。

## lstm

最后我们看看lstm，lstm比较重要的几个参数：batch_size为4，windows_size为3倍的predict_time，num_unit为3倍的predict_time，学习速率为0.01。

![image-20181112153242744](https://ws3.sinaimg.cn/large/006tNbRwly1fx5bd8zx0ej30fx0bujst.jpg)

结果PCT为0.043834，time为7.16s。

接下来我们将介绍周期性预测。

### 周期性预测

### LR

![image-20181112153745252](https://ws1.sinaimg.cn/large/006tNbRwly1fx5bihlk9dj30fs0bq75q.jpg)

结果是PCT为0.044276，时间消耗为1.51s。

### arima

![image-20181112154057873](https://ws2.sinaimg.cn/large/006tNbRwly1fx5blty7wsj30g90bxwfx.jpg)

PCT为0.047879，time为1.73s。

### bp神经网络

![image-20181112154221004](https://ws1.sinaimg.cn/large/006tNbRwly1fx5bna2xy3j30fy0bzdha.jpg)

PCT为0.042720，time为1.43s。

### lstm

![image-20181112154336287](https://ws1.sinaimg.cn/large/006tNbRwly1fx5bokrqsmj30g20bwabi.jpg)

PCT为0.041202，time为6.28s。

## 总结

### 非周期性预测



|     模型     | 时间开销 |  准确率  |
| :----------: | :------: | :------: |
|      LR      |  1.27s   | 0.085063 |
|    ARIMA     |  1.43s   |  0.092   |
| 浅层神经网络 |  1.56s   | 0.087210 |
|     LSTM     |  7.16s   | 0.043834 |

### 周期性预测



|     模型     | 时间开销 |  准确率  |
| :----------: | :------: | :------: |
|      LR      |  1.51s   | 0.044276 |
|    ARIMA     |  1.73s   | 0.047879 |
| 浅层神经网络 |  1.43s   | 0.042720 |
|     LSTM     |  6.28s   | 0.041202 |

通过上面两种方法，可以得到，在时间序列具有周期性的情况下，用周期性预测的方法可以极大程度上提高准确率。