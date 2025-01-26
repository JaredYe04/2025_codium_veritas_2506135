#数据集格式：Name,Sex,Team,NOC,Year,City,Sport,Event,Medal
#为了探索不同国家擅长的体育项目，我们需要对数据集进行分析，对于同一个项目(以Sport为单位)，所有国家获得的奖牌中，根据目标国家奖牌数的占比确定该项目是否是目标国家擅长的项目。
#summerOly_athletes.csv
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
#不同国家擅长的体育项目
#目标国家
target_country='United States'#对应列为Team

#目标国家奖牌数
#Medal列中，No medal表示没有奖牌，Bronze表示铜牌，Silver表示银牌，Gold表示金牌
#筛选出目标国家不同项目的奖牌数，注意要排除No medal
target_country_medals=data[(data['Team']==target_country)&(data['Medal']!='No medal')].groupby('Sport').size()
#所有国家奖牌数
all_country_medals=data[data['Medal']!='No medal'].groupby('Sport').size()
#目标国家奖牌数占比
medal_rate=target_country_medals/all_country_medals
#排序
medal_rate=medal_rate.sort_values(ascending=False)


#如果小于0.005，不显示
medal_rate=medal_rate[medal_rate>0.005]
#只显示前20个
medal_rate=medal_rate[:20]
#绘制图表
plt.figure(figsize=(10,6))
sns.barplot(x=medal_rate.values,y=medal_rate.index)
plt.title('Percentage of Medals of Different Sports in '+target_country)
medal_rate.to_csv('./data/美国擅长的体育项目.csv')
plt.show()

#导出数据

pass



#用同样的方法，分别计算每个国家擅长的体育项目，导出csv文件
#列为Team，Sport，Adeptness
#Adeptness表示擅长程度，即该国家在该项目的奖牌数占所有国家奖牌数的比例
#数据集格式：Team,Sport,Adeptness
#country_adeptness.csv
#读取数据
data=pd.read_csv('./data/summerOly_athletes.csv')

#数据预处理
#去除重复值
data.drop_duplicates(inplace=True)
#去除缺失值
data.dropna(inplace=True)

#数据分析
#不同国家擅长的体育项目

# #注意，Team字段可能有一些冗余字符，例如South Korea可能会有-2 -3 -4 -11之类的-数字，所以需要截断至-之前的字符

# data['Team']=data['Team'].apply(lambda x:x.split('-')[0])

# countries=data['Team'].unique()
countries=data['NOC'].unique()
result=[]

idx=0
for country in countries:
    #目标国家
    target_country=country

    #目标国家奖牌数
    #Medal列中，No medal表示没有奖牌，Bronze表示铜牌，Silver表示银牌，Gold表示金牌
    #筛选出目标国家不同项目的奖牌数，注意要排除No medal
    target_country_medals=data[(data['NOC']==target_country)&(data['Medal']!='No medal')].groupby('Sport').size()
    #所有国家奖牌数
    all_country_medals=data[data['Medal']!='No medal'].groupby('Sport').size()
    #目标国家奖牌数占比
    medal_rate=target_country_medals/all_country_medals
    #排序
    medal_rate=medal_rate.sort_values(ascending=False)
    #添加到结果中
    for sport in medal_rate.index:
        result.append([target_country,sport,medal_rate[sport]])
    idx+=1
    print('正在处理',idx,',共',len(countries),'个国家')
        
#导出结果
result=pd.DataFrame(result,columns=['NOC','Sport','Adeptness'])
result.to_csv('./data/country_adeptness.csv',index=False)