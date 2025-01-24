#检验summerOly_medal_counts.csv里面，各国的每一届奖牌总数，与summerOly_athletes.csv里面，所有运动员加起来的奖牌总数是否一致

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#读取数据
data=pd.read_csv('./data/summerOly_athletes.csv')

#数据预处理
#去除重复值
data.drop_duplicates(inplace=True)
#去除缺失值
data.dropna(inplace=True)


mapping=pd.read_csv('./data/noc_region.csv')
#NOC与国家名字的映射表

#检验summerOly_medal_counts.csv里面，某国每一届奖牌总数，与summerOly_athletes.csv里面，该国当届所有运动员加起来的奖牌总数是否一致

#读取数据
medal_counts=pd.read_csv('./data/summerOly_medal_counts.csv')
#检验

passed=[]
failed=[]
for i in range(len(medal_counts)):
    NOC=medal_counts.loc[i,'NOC']
    name=NOC
    if NOC not in mapping['Country'].values:
        #print(NOC)
        continue
    NOC=mapping[mapping['Country']==NOC]['NOC'].values[0]
    year=medal_counts.loc[i,'Year']
    #该国该年奖牌总数
    total_medals=medal_counts.loc[i,'Total']
    #该国该年所有运动员奖牌总数
    athletes_medals=data[(data['NOC']==NOC)&(data['Year']==year)&(data['Medal']!='No medal')].shape[0]
    if total_medals!=athletes_medals and athletes_medals!=0:
        print(name,NOC,year,total_medals,athletes_medals)
        failed.append((name,NOC,year,total_medals,athletes_medals))
    else:
        #print(name,NOC,year,'pass')
        passed.append((name,NOC,year))
        
        
#画饼图，显示检验结果
plt.figure(figsize=(6,6))
plt.pie([len(passed),len(failed)],labels=['passed','failed'],autopct='%1.1f%%')
plt.title('Check Results')
plt.show()
# pass