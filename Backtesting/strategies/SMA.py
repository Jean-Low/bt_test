from backtesting import evaluateHist, evaluateTick
from strategy import Strategy
from order import Order
from event import Event
from riskSignal import Signal
import numpy as np
import pickle

#import do modelo
import Model

class SMA(Strategy):
    
  def __init__(self):
        
    self.name = "SMA"
    self.prices = []
    self.last_price = None
    self.alpha = 0.005
    with open ("model.pkl", "rb") as file:
      self.model = pickle.load(file)

  def predict(self):
    prices = np.array(self.prices)
    prices = np.reshape(prices, (1, self.model.sample,1))
    return self.model.Predict(prices)

  def push(self, event):
    print("push " + self.name)
    #Classe que ser[a retornada para o modelo de risco
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
