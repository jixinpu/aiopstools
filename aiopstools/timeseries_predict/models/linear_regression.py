#-*- encoding: utf-8 -*-

from sklearn import linear_model

class Linear_regression(object):
    def __init__(self, predict_time):
        self.predict_time = int(predict_time)

    def train(self, data, x, y):
        regr = linear_model.LinearRegression()
        x_list = []
        for i in range(len(y)):
            x_list.append([i])

        regr.fit(x_list, y)
        return regr
    
    def predict(self, regr, y):
        time_predict = []
        for i in range(self.predict_time):
            time_predict.append([i + len(y)])
        predict_outcome = regr.predict(time_predict)
        predict_data = []
        for i in range(self.predict_time):
            predict_data.append(round(predict_outcome[i], 2))
        return predict_data
