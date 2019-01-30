#-*- encoding: utf-8 -*-

from pybrain.structure import *
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

class BP_network(object):
    def __init__(self, predict_time):
        self.predict_time = int(predict_time)

    def train(self, data, x, y):
        # 输入、隐藏层和输出层的节点数
        in_num = self.predict_time
        out_num = self.predict_time
        hidden_num = self.predict_time * 2

        # 生成样本
        train_data_x = []
        train_data_y = []
        if len(y) > (3*(in_num+out_num)+1):
            for i in range(len(y)-2*self.predict_time):
                data_x = y[i:(i+in_num)]
                data_y = y[(i+in_num):(i+in_num+out_num)]
                train_data_x.append(data_x)
                train_data_y.append(data_y)
        else:
            print('few data')
            return

		# 建立神经网络fnn
        fnn = FeedForwardNetwork()  
        # 设立三层，一层输入层（别名为inLayer），一层隐藏层，一层输出层
        inLayer = LinearLayer(in_num, name='inLayer')
        hiddenLayer = SigmoidLayer(hidden_num, name='hiddenLayer0')
        outLayer = LinearLayer(out_num, name='outLayer')  
  
        # 将三层都加入神经网络（即加入神经元)
        fnn.addInputModule(inLayer)  
        fnn.addModule(hiddenLayer)  
        fnn.addOutputModule(outLayer)  
  
        # 建立三层之间的连接
        in_to_hidden = FullConnection(inLayer, hiddenLayer)  
        hidden_to_out = FullConnection(hiddenLayer, outLayer)  
  
        # 将连接加入神经网络
        fnn.addConnection(in_to_hidden)  
        fnn.addConnection(hidden_to_out)  
  
        # 让神经网络可用
        fnn.sortModules()  

        ds = SupervisedDataSet(in_num, out_num)
        for i in range(len(train_data_x)):
            ds.addSample(train_data_x[i], train_data_y[i])

        trainer = BackpropTrainer(fnn, ds, verbose = True, learningrate=0.01)
        trainer.trainUntilConvergence(maxEpochs=100)
        return fnn
    
    def predict(self, fnn, y):
        # 预测结果
        prediction = fnn.activate(y[-self.predict_time:])
        return prediction
