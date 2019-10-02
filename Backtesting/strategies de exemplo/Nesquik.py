from backtesting import evaluateHist, evaluateTick
from strategy import Strategy
from order import Order
from event import Event
from riskSignal import Signal
import numpy as np
import pickle
import sys

class Nesquik(Strategy):
    
  def __init__(self, model):
        
    self.name = "Nesquik"
    self.prices = []
    self.last_price = None
    self.alpha = 0.01

    print("Init " + self.name)
    print("Using " + model)
    
    exec("from models.{0} import {0}".format(model))
    exec("sys.modules['{0}'] = sys.modules['models.{0}']".format(model))

    with open ("./models/{0}.pkl".format(model.lower()), 'rb') as file:
      self.model = None
      print(file)
      self.model = pickle.load(file)

  def predict(self):
    prices = np.array(self.prices)
    prices = np.reshape(prices, (1, self.model.sample,1))
    return self.model.Predict(prices)

  def push(self, event):
    print("push " + self.name)
    #Classe que sera retornada para o modelo de risco
    signals = []
    #Guarda os ultimos precos
    price = event.price
    self.prices.append(price)
    #Verifica se tem prices suficientes para o predict do model
    if len(self.prices) == self.model.sample:
      prediction = self.predict()
      #Com a prediction toma uma decisao
      if prediction[0][0] > price + self.alpha:
        #Adiciona a decisao na lista de decisoes
        signals.append(Signal(event.instrument, -1))
      elif prediction[0][0] < price - self.alpha:
        #Adiciona a decisao na lista de decisoes
        signals.append(Signal(event.instrument, 1))
      del(self.prices[0])

    return signals

#print(evaluateTick(SMA(), {'PETR4':'2018-03-07.csv'}))
