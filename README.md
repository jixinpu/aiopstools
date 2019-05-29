# aiopstools
**Aiopstools** is a toolkit for aiops. It realizes some ops scenes by using ai. You can import modules easily to achieve functions.  

[ 中文文档](https://github.com/jixinpu/aiopstools/blob/master/README_CN.md)

## Installation

```
git clone https://github.com/jixinpu/aiopstools.git
cd aiopstools
python setup.py install
```

Python2 and python3 are all supported.

## Modules

Aiopstools provides capabilities:

[ Anomaly detection](https://github.com/jixinpu/aiopstools/tree/master/docs/anomal_detection_test.md)

[Alarm convergence](https://github.com/jixinpu/aiopstools/tree/master/docs/alarm_convergence_test.md)

[Time Series Forecasting Method](https://github.com/jixinpu/aiopstools/tree/master/docs/timeseries_predict_test.md)

[Association analysis for alarms](https://github.com/jixinpu/aiopstools/tree/master/docs/alarm_association_test.md)

## Versions

**2018.12.01** Time series forecasting、anomaly detection、alarm convergence；

**2019.2.15** Association analysis； 

## Supports

If have interest in aiops, you can contact me. My email is jixinpu@126.com

In addition to this, i have a special column about aiops, which updates recent progress in the field. The url of special column is https://zhuanlan.zhihu.com/c_178702079.

## Problems

1.If you use python3, please altering the file's content.

```
/site-packages/pybrain/tools/functions.py", line 4, expm2 to expm.
```




