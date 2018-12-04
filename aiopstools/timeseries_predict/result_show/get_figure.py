# -*- encoding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def get_figure(value_list, predict_data, truth_data):
    timestamp_list = np.arange(0, len(value_list), 1)
    train_line, = plt.plot(timestamp_list, value_list, color='black', label='train')
    predict_timestamp_list = np.arange(len(value_list), (len(value_list) + len(predict_data)), 1)

    predict_line, = plt.plot(predict_timestamp_list, predict_data, color='red', label='predict')
    truth_line, = plt.plot(predict_timestamp_list, truth_data, color='blue', label='truth')
    plt.legend(handles=[train_line, predict_line, truth_line,], labels=['train', 'predict', 'truth'], loc='best')
    plt.ylabel('values')
    plt.xlabel('Times(h)')
    plt.show()