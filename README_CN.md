# aiopstools
aiopstools是aiops领域公开的工具包，里面提供的功能包括：
- 时间序列的预测；
- 异常检测；
- 报警收敛；
- 报警关联分析；

## 安装
目前既支持python2，也支持python3。
```
git clone https://github.com/jixinpu/aiopstools.git
cd aiopstools
python setup.py install
```

## 功能模块

目前我们提供的功能如下：

[时间序列异常检测](https://github.com/jixinpu/aiopstools/tree/master/docs/anomal_detection_test.md)

[报警收敛](https://github.com/jixinpu/aiopstools/tree/master/docs/alarm_convergence_test.md)

[时间序列预测](https://github.com/jixinpu/aiopstools/tree/master/docs/timeseries_predict_test.md)

[报警关联分析](https://github.com/jixinpu/aiopstools/tree/master/docs/alarm_association_test.md)

## 版本更新

**2018.12.01** 时间序列预测、异常检测、报警收敛；

**2019.2.15** 微软论文报警关联分析； 

### 交流
如果对aiops感兴趣，可以和我进行交流，我的邮箱：

jixinpu@126.com

除此之外，我还建立了aiops的知乎专栏，上面会经常更新一些aiops的最新研究进展，知乎专栏地址：

https://zhuanlan.zhihu.com/c_178702079

## 问题

1.如果您使用python3，需要将/site-packages/pybrain/tools/functions.py", line 4的expm2改成expm。