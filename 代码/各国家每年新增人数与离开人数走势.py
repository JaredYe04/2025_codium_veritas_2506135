import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('./data/summerOly_athletes.csv')

# 以每个国家的每个项目为单位，统计每年新增的人数和离开的人数

#1896年为第一届奥运会，从下一届开始统计
years = data['Year'].unique()

#结果
result = []
#统计每个国家的每个项目
idx=0
for country in data['NOC'].unique():
    idx+=1
    
    idx2=0
    for sport in data['Sport'].unique():
        idx2+=1
        print('正在处理第{}个国家，共{}个国家;第{}个项目，共{}个项目：'.format(idx,len(data['NOC'].unique()),idx2,len(data['Sport'].unique())))
        for year in years:
            #本届数据
            current_data = data[(data['Year'] == year) & (data['NOC'] == country) & (data['Sport'] == sport)]
            #上一届数据
            #上一届不一定是-4，因为有可能有一届奥运会没有举办
            last_year = year - 4
            # if last_year not in years:
            #     last_year = year - 2
            last_data = data[(data['Year'] == last_year) & (data['NOC'] == country) & (data['Sport'] == sport)]
            #新增人数
            new_athletes = len(set(current_data['Name']) - set(last_data['Name']))
            #离开人数
            leave_athletes = len(set(last_data['Name']) - set(current_data['Name']))
            
            result.append([country,sport,year,new_athletes,leave_athletes])
result = pd.DataFrame(result,columns=['NOC','Sport','Year','New','Leave'])

result.to_csv('./data/athlete_variation.csv',index=False)