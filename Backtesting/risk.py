from wallet import Wallet
from order import Order

class Risk(): #should i call it Trader? or something else?

  def __init__(self,_ts):
    self.wallet = Wallet()
    self.ts = _ts
    pass

  
  def set_var(self, value): #values are in cents
    var = int(value) 
    self.var = var

  def send(self, signals):
    #print("im getting the signal at least")
    #here is where we make the magic

    #for now i just apply the signal value as a order quantity and that is it (as it was on exampleMarcelo.py)

    orders = []
    for signal in signals:
          orders.append(Order(signal.instrument, signal.value,0))
    self.ts.submit(None,orders)
    
