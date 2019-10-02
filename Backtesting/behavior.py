

'''
from StrategyMA import SMA
from exampleMarcelo import RSI

from backtesting import MarketData, evaluateMult

#print(SMA)
#print(RSI)

strategy_list = [SMA(),RSI()]
type_list = [MarketData.TICK, MarketData.HIST]
file_list = [{'PETR4':'2018-03-07.csv' }, {'IBOV':'^BVSP.csv'}]

print (evaluateMult(strategy_list, type_list, file_list))
'''

from backtesting import MarketData, evaluateMult, evaluateTick
import os
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk("./strategies"):
    for file in f:
        if file[-3:] == ".py":
            files.append(file[:-3])

strategy_list = []


for f in files:
    exec("from strategies.{0} import {0}".format(f))
    exec("strategy_list.append({0}())".format(f))

#type_list = [MarketData.HIST, MarketData.TICK]
#file_list = [{'IBOV':'^BVSP.csv'}, {'PETR4':'2018-03-07.csv' }]

type_list = []
file_list = []

for s in strategy_list:
    print(s.name)
    type_list.append(MarketData.TICK)
    file_list.append({'PETR4' : '2018-03-07.csv'})

response = evaluateMult(strategy_list, type_list, file_list)

for summary in response:
    print("Summary")
    print(summary)
