#统计不同国家每届比赛对每个项目派出的人数
#数据来源summerOly_athletes.csv

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

#数据分析
#不同国家每届比赛对每个项目派出的人数
#目标国家
target_country='USA'#对应列为NOC

target_sport='Athletics'#对应列为Sport

#历届比赛派出的人数

#筛选出目标国家不同项目的人数
target_country_athletes=data[(data['NOC']==target_country)&(data['Sport']==target_sport)].groupby('Year').size()

#绘制图表
plt.figure(figsize=(10,6))
sns.barplot(x=target_country_athletes.index,y=target_country_athletes.values)
plt.title('Number of Athletes of '+target_sport+' in '+target_country+' in Different Years')

plt.show()


pass



#根据以上思路，对每个国家的每个项目进行同样的统计，导出csv文件
#列为NOC，Sport，Year，Athletes
#数据集格式：NOC,Sport,Year,Athletes

result=[]

#所有国家
countries=data['NOC'].unique()
#所有项目
sports=data['Sport'].unique()
idx=0
for country in countries:
    idx+=1
    print('第',idx,'个国家','共',len(countries),'个国家')
    for sport in sports:
        #筛选出目标国家不同项目的人数
        country_sport_athletes=data[(data['NOC']==country)&(data['Sport']==sport)].groupby('Year').size()
        #添加到结果中
        for year in country_sport_athletes.index:
            result.append([country,sport,year,country_sport_athletes[year]])
            
#转换为DataFrame
result=pd.DataFrame(result,columns=['NOC','Sport','Year','Athletes'])
#导出csv文件
result.to_csv('./data/n_participants.csv',index=False)