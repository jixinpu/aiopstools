#-*- encoding: utf-8 -*-

from .linear_regression import Linear_regression
from .ann import BP_network
from .arima import ARIMAModel
from .lstm import LSTM

__factory = {
    'lr': Linear_regression,
    'ann': BP_network,
    'arima': ARIMAModel,
	'lstm': LSTM
}

def names():
    return sorted(__factory.keys())

def create(name, *args, **kwargs):
    if name not in __factory:
        raise KeyError("Unknown model:", name)
    return __factory[name](*args, **kwargs)
