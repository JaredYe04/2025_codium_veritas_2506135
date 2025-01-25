#现在有一个文件，里面记录着历届奥运会的各个国家排名
#数据保持不变，但是现在需要换一种保存方式
#以下是原本的数据格式
# Rank	NOC	Gold	Silver	Bronze	Total	Year
# 1	United States	11	7	2	20	1896
# 2	Greece	10	18	19	47	1896
# 3	Germany	6	5	2	13	1896
# 4	France	5	4	2	11	1896
# 5	Great Britain	2	3	2	7	1896
# 6	Hungary	2	1	3	6	1896
# 1	France	27	39	37	103	1900
# 2	United States	19	14	15	48	1900
# 3	Great Britain	15	7	9	31	1900
# 4	Mixed team	8	5	6	19	1900
# 1	United States	76	78	77	231	1904
# 2	Germany	4	5	6	15	1904
# 3	Canada	4	1	1	6	1904
# 4	Cuba	3	0	0	3	1904
# 5	Hungary	2	1	1	4	1904

#现在需要将这个数据保存为以下格式，记录每个国家每年的奖牌数
# Year	United States	China	Russia  Japan ...
# 2016	100 101 101 100
# 2017	100 101 101 100
# 2018	100 101 101 100
# 2019	100 101 101 100

#请将原始数据保存为新的格式
import pandas as pd
import numpy as np
#读取数据
data=pd.read_csv('./data/奥运排名+预测.csv')
#将数据转换为新的格式
#获取所有国家的名称
countries=['United States','China','Japan','Australia','France','Netherlands','Great Britain','South Korea','Italy','Germany','New Zealand','Canada','Uzbekistan','Hungary','Spain','Sweden']
#获取所有年份
years=data['Year'].unique()
years=years[years>=1984]
#创建新的数据集
new_data=pd.DataFrame(columns=['Year']+list(countries))
#填充数据
for year in years:
    #获取本年的数据
    current_data=data[data['Year']==year]
    #创建新的一行
    new_row={'Year':year}
    #填充数据
    for country in countries:
        #获取本国的数据
        current_country_data=current_data[current_data['NOC']==country]
        if len(current_country_data)==0:
            new_row[country]=0
        else:
            new_row[country]=current_country_data['Total'].values[0]
    #添加到数据集中
    new_data=new_data._append(new_row,ignore_index=True)
    
    
    
#筛选数据
new_data=new_data[new_data['Year']>=1980]

#重新排序列
new_data=new_data[['Year']+countries]

#保存数据
new_data.to_csv('./data/奥运排名+预测_新格式.csv',index=False)




