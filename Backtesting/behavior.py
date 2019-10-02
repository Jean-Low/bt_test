
import os
from backtesting import MarketData, evaluateMult, evaluateTick



strategy_files = []
# r=root, d=directories, f = files
for r, d, f in os.walk("./strategies"):
    for file in f:
        if file[-3:] == ".py":
            strategy_files.append(file[:-3]) 

sm_relations = {}
with open("relations.txt", "r") as file:
    line = file.readline()
    while line:
        relat = line.strip('\n').split(':')
        sm_relations[relat[0]] = relat[1]
        line = file.readline()

print(sm_relations)


strategy_list = []

for f in strategy_files:
    print("sou um " + f)
    print(type(f))
    exec("from strategies.{0} import {0}".format(f))
    exec("strategy_list.append({0}(sm_relations['{0}']))".format(f))
    

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
