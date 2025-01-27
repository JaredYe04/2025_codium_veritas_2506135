#我们要统计，所有作为东道主的国家，派遣了多少名运动员参加别的东道主国家的奥运会。
#最终结果是一个表格，表格的每一行有5个字段，分别是：

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('./data/summerOly_hosts.csv')
# Year,Host
# 1896," Athens, Greece"
# 1900," Paris, France"
# 1904," St. Louis, United States"
# 1908," London, United Kingdom"
# 1912," Stockholm, Sweden"
# 1920," Antwerp, Belgium"

#提取出Year,City,Country
columns=['Year','City','Country']
hosts=pd.DataFrame(columns=columns)
hosts['Year']=data['Year']
hosts['City']=data['Host'].str.split(',').str[0]
hosts['Country']=data['Host'].str.split(',').str[1]
NOCs=['GRE','FRA','USA','GBR','SWE','BEL','FRA','NED','USA','GER','GBR','FIN','AUS','ITA','JPN','MEX','FRG','CAN','URS','USA','KOR','ESP','USA','AUS','GRE','CHN','GBR','BRA','JPN','FRA','USA','AUS']
hosts['NOC']=NOCs
print(hosts)

#summerOly_athletes.csv
data = pd.read_csv('./data/summerOly_athletes.csv')

#筛选出所有来自曾经的东道主国家的运动员
result = data[data.NOC.isin(hosts.NOC)]

#把东道主之间两两组合，可以得到所有派遣运动员的情况，注意区分source和dest，应当

from itertools import combinations
combs=list(combinations(hosts.NOC.unique(),2))
#去除自己和自己组合的情况
combs=[comb for comb in combs if comb[0]!=comb[1]]
combs.extend([(comb[1],comb[0]) for comb in combs])

# #交换combs中的source和dest，得到inner_combs
# inner_combs=[]
# for comb in combs:
#     inner_combs.append((comb[1],comb[0]))
# combs=inner_combs

#统计每一对东道主之间的运动员数量
results=[]
for comb in combs:
    source=comb[0]
    dest=comb[1]
    value=0
    #统计source派往dest的运动员数量，注意data的Year字段可以通过查询hosts表，得到该年份的东道主的NOC,从而判断是否是source派往dest的运动员
    #所以筛选出dest对应的Year
    destYears=hosts[hosts.NOC==dest]['Year']
    #print(destYears)  
    #筛选出data中年份为destYears的数据
    destData=data[data.Year.isin(destYears)]
    #筛选出NOC为source的数据
    sourceData=destData[destData.NOC==source]
    #print(sourceData)
    value=sourceData.shape[0]
    results.append([source,dest,value])
    
print(results)

#保存结果
result=pd.DataFrame(results,columns=['Source','Dest','Value'])

result.to_csv(f'./data/hosts_athletes.csv',index=False)
#Source	Dest	Value
