#-*- encoding: utf-8 -*-

import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm

class ARIMAModel(object):
    def __init__(self, predict_time):
        self.predict_time = int(predict_time)

    def train(self, dta, x, y):
        predict_data = []
        if np.max(y) - np.min(y) == 0:
            for i in range(0, self.predict_time):
                predict_data.append(round(np.max(y),2))
            return predict_data
       	
        """
        for i in range(0, len(mydata_tmp)):
            mydata_tmp[i] = math.log(mydata_tmp[i])
        """
        """
        p为ARMA模型的参数，一般p去小于length/10的数
        但是由于数据的问题，所以分情况设置
        """
        res = sm.tsa.arma_order_select_ic(dta, max_ar=7, max_ma=0,ic=['bic'],trend='nc')
        p = res.bic_min_order[0]
        q = res.bic_min_order[1]
        # 建立ARMA模型
        # freq为时间序列的偏移量
        try:
            try:
                model_tmp = ARIMA(dta, order=(p,1,q))
                # method为css-mle
                #model = model_tmp.fit(disp=-1)
                model = model_tmp.fit(disp=-1, method='mle')
                return model
            except:
                model_tmp = ARIMA(dta, order=(1,1,1))
                model = model_tmp.fit(disp=-1, method='mle')
                return model
        except:
            return
    
    def predict(self, model, y):
        predict_outcome = model.forecast(self.predict_time)
        return predict_outcome[0]
