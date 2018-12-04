#-*- encoding: utf-8 -*-

from .fitting import Ewma
from .iforest import IForest
from .statistics import POP, POP_Amplitude, Tail

__factory = {
    'pop': POP,
    'amplitude': POP_Amplitude,
    'tail': Tail,
	'iforest': IForest,
    'fitting': Ewma
}

def names():
    return sorted(__factory.keys())

def create(name, *args, **kwargs):
    if name not in __factory:
        raise KeyError("Unknown model:", name)
    return __factory[name](*args, **kwargs)