#summerOly_medal_counts.csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#读取数据
data=pd.read_csv('./data/summerOly_medal_counts.csv')

countries=data['NOC'].unique()


data=pd.read_csv('./data/noc_region.csv')

#逐一检验，如果发现noc_regions.csv里面没有的国家，输出国家名

for country in countries:
    if country not in data['Country'].values:
        print(country)
        
        
NOCs=pd.read_csv('./data/summerOly_athletes.csv')['NOC'].unique()
#检查一下NOCs里面有没有不在noc_regions.csv里面的国家
for NOC in NOCs:
    if NOC not in data['NOC'].values:
        print(NOC)
