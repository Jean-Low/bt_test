# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 22:11:38 2019

@author: edufe
"""

import numpy as np

class Model:
    def __init__(self, sample, predsize):
        
        self.name = "MA"
        self.modeltype = "Regressor"
        
        self.sample = sample
        self.predsize = predsize 
        
    def FirstTrain(self, TrainData, TestData):
        
        Predsize = self.predsize
        Sample = self.sample
        
        Train_X = []
        Train_Y = []
        
        Test_X = []
        Test_Y = []
        
        #Para o Treino
        for Train in TrainData:
            Train = Train["Preço"].to_list()
            for i in range(len(Train)):
                if i > Sample and len(Train)-i > Predsize:
                    Train_X.append(np.array(Train[i-Sample:i]))
                    Train_Y.append(np.array(Train[i: i+Predsize]))
        
        Train_X, Train_Y = np.array(Train_X), np.array(Train_Y)
        Train_X = np.reshape(Train_X, (Train_X.shape[0], Sample, 1))
        Train_Y = np.reshape(Train_Y, (Train_Y.shape[0], Predsize))
        
        self.Train_X = Train_X
        self.Train_Y = Train_Y
                
        #Para o Teste
        for Test in TestData:
            Test = Test["Preço"].to_list()
            for i in range(len(Test)):
                if i > Sample and len(Test)-i > Predsize:
                    Test_X.append(np.array(Test[i-Sample:i]))
                    Test_Y.append(np.array(Test[i: i+Predsize]))
                    
        Test_X, Test_Y = np.array(Test_X), np.array(Test_Y)
        Test_X = np.reshape(Test_X, (Test_X.shape[0], Sample, 1))
        Test_Y = np.reshape(Test_Y, (Test_Y.shape[0], Predsize))
        
        self.Test_X = Test_X
        self.Test_Y = Test_Y
    
    def Train(self, Train_X, Train_Y):
  
        pass
        
    def Predict(self, Predict_X):
        
        if isinstance(Predict_X, np.ndarray):
            Shape = Predict_X.shape
        else:
            Shape = np.array(Predict_X.shape).shape
        
        if len(Shape) == 2:
            
            Predict_Y = [np.mean(Predict_X)]*self.predsize
            
        if len(Shape) == 3:
            Predict_Y = []
            
            for ThisSample in Predict_X:
                Predict_Y.append([np.mean(ThisSample)]*self.predsize)
                
        else:
            raise ValueError("Invalid Array Shape")
                
        return np.array(Predict_Y)