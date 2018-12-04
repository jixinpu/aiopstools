# -*- encoding: utf-8 -*-

from os import path

import numpy as np
import tensorflow as tf

from tensorflow.contrib.timeseries.python.timeseries import estimators as ts_estimators
from tensorflow.contrib.timeseries.python.timeseries import model as ts_model
from tensorflow.contrib.timeseries.python.timeseries import NumpyReader


class LSTMModel(ts_model.SequentialTimeSeriesModel):
    def __init__(self, predict_time, num_units, num_features, dtype=tf.float32):
        super(LSTMModel, self).__init__(
            train_output_names=["mean"],
            predict_output_names=["mean"],
            num_features=num_features,
            dtype=dtype)

        self._num_units = num_units
        self.predict_time = predict_time

        self._lstm_cell = None
        self._lstm_cell_run = None
        self._predict_from_lstm_output = None

    def initialize_graph(self, input_statistics):
        super(LSTMModel, self).initialize_graph(input_statistics=input_statistics)
        self._lstm_cell = tf.nn.rnn_cell.LSTMCell(num_units=self._num_units)

        self._lstm_cell_run = tf.make_template(
            name_="lstm_cell",
            func_=self._lstm_cell,
            create_scope_now_=True)

        self._predict_from_lstm_output = tf.make_template(
            name_="predict_from_lstm_output",
            func_=lambda inputs: tf.layers.dense(inputs=inputs, units=self.num_features),
            create_scope_now_=True)

    def get_start_state(self):
        return (
            tf.zeros([], dtype=tf.int64),
            tf.zeros([self.num_features], dtype=self.dtype),
            [tf.squeeze(state_element, axis=0)
             for state_element
             in self._lstm_cell.zero_state(batch_size=1, dtype=self.dtype)])

    def _transform(self, data):
        mean, variance = self._input_statistics.overall_feature_moments
        return (data - mean) / variance

    def _de_transform(self, data):
        mean, variance = self._input_statistics.overall_feature_moments
        return data * variance + mean

    def get_start_state(self):
        return (
            tf.zeros([], dtype=tf.int64),
            tf.zeros([self.num_features], dtype=self.dtype),
            [tf.squeeze(state_element, axis=0)
             for state_element
             in self._lstm_cell.zero_state(batch_size=1, dtype=self.dtype)])

    def _exogenous_input_step(self, current_times, current_exogenous_regressors, state):
        raise NotImplementedError("Exogenous inputs are not implemented for this example.")

    def _filtering_step(self, current_times, current_values, state, predictions):
        state_from_time, prediction, lstm_state = state
        with tf.control_dependencies(
                [tf.assert_equal(current_times, state_from_time)]):
            transformed_values = self._transform(current_values)
            predictions["loss"] = tf.reduce_mean(
                (prediction - transformed_values) ** 2, axis=-1)
            new_state_tuple = (current_times, transformed_values, lstm_state)
        return (new_state_tuple, predictions)

    def _imputation_step(self, current_times, state):
        return state

    def _prediction_step(self, current_times, state):
        _, previous_observation_or_prediction, lstm_state = state
        lstm_output, new_lstm_state = self._lstm_cell_run(
            inputs=previous_observation_or_prediction, state=lstm_state)
        next_prediction = self._predict_from_lstm_output(lstm_output)
        new_state_tuple = (current_times, next_prediction, new_lstm_state)
        return new_state_tuple, {"mean": self._de_transform(next_prediction)}


class LSTM(object):
    def __init__(self, predict_time):
        self.predict_time = int(predict_time)

    def _get_timeseries(self, y):
        # 将x进行初始化成0到len(y)的numpy数组
        x = np.array(range(len(y)))
        # 生成时间序列
        data = {
            tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
            tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
        }
        return data

    def train(self, ori_data, x, y):
        data = self._get_timeseries(y)
        reader = NumpyReader(data)

        # 历史数据必须超过三个预测时间
        if len(y) > 3*self.predict_time:
            # tf.contrib.timeseries.RandomWindowInputFn会在reader的所有数据中，随机选取窗口长度为window_size的序列，
            # 并包装成batch_size大小的batch数据。换句话说，一个batch内共有batch_size个序列，每个序列的长度为window_size。
            train_input_fn = tf.contrib.timeseries.RandomWindowInputFn(
                reader, batch_size=4, window_size=3*self.predict_time)

            # 定义lstm模型，num_features = 1表示单变量时间序列，
            # num_units=n表示使用隐层(记忆和储存过去状态的节点个数)为n大小的LSTM模型。
            estimator = ts_estimators.TimeSeriesRegressor(
                model=LSTMModel(self.predict_time, num_features=1, num_units=3*self.predict_time),
                optimizer=tf.train.AdamOptimizer(0.001))
            # 在原有len(y)基础上预测
            estimator.train(input_fn=train_input_fn, steps=len(y))
            return estimator
        else:
            print('few data')

    def predict(self, estimator, y):
        data = self._get_timeseries(y)
        reader = NumpyReader(data)
        evaluation_input_fn = tf.contrib.timeseries.WholeDatasetInputFn(reader)
        evaluation = estimator.evaluate(input_fn=evaluation_input_fn, steps=1)
        # 预测predict_time的步长
        (predictions,) = tuple(estimator.predict(
            input_fn=tf.contrib.timeseries.predict_continuation_input_fn(
                evaluation, steps=self.predict_time)))

        # 预测时间
        # predicted_times = predictions['times']
        predicted = predictions["mean"]
        outcome = []
        for i in range(len(predicted)):
            outcome.append(predicted[i][0])
        return outcome
