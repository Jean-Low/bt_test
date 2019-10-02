# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 22:11:38 2019

@author: edufe
"""

import numpy as np

class Model_MA:
    def __init__(self, sample, predsize, TrainData, TestData):
        
        self.name = "MA"
        self.modeltype = "Regressor"
        
        self.sample = sample
        self.predsize = predsize 
    
        #Separa os dados entre X e Y para o modelo
        #Dados das listas X devem ter o formato do input do modelo
        #Dados das listas Y deve ter o formato do predict do modelo
        Train_X = []
        Train_Y = []
        
        Test_X = []
        Test_Y = []
        
        #Para o Treino
        for Train in TrainData:
            Train = Train["Preço"].to_list()
            for i in range(len(Train)):
                if i > sample and len(Train)-i > predsize:
                    Train_X.append(np.array(Train[i-sample:i]))
                    Train_Y.append(np.array(Train[i: i+predsize]))
        
        Train_X, Train_Y = np.array(Train_X), np.array(Train_Y)
        Train_X = np.reshape(Train_X, (Train_X.shape[0], sample, 1))
        Train_Y = np.reshape(Train_Y, (Train_Y.shape[0], predsize))
        
        self.Train_X = Train_X
        self.Train_Y = Train_Y
                
        #Para o Teste
        for Test in TestData:
            Test = Test["Preço"].to_list()
            for i in range(len(Test)):
                if i > sample and len(Test)-i > predsize:
                    Test_X.append(np.array(Test[i-sample:i]))
                    Test_Y.append(np.array(Test[i: i+predsize]))
                    
        Test_X, Test_Y = np.array(Test_X), np.array(Test_Y)
        Test_X = np.reshape(Test_X, (Test_X.shape[0], sample, 1))
        Test_Y = np.reshape(Test_Y, (Test_Y.shape[0], predsize))
        
        self.Test_X = Test_X
        self.Test_Y = Test_Y
        
        #Monta o modelo se for aplicavel
        
    def FirstTrain(self):
        
        pass
    
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