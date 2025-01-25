#现在有三个文件，“各国奖牌预测_悲观.csv”、“各国奖牌预测_乐观.csv”、“各国奖牌预测_中等.csv”，请你完成以下任务：
# 1. 读取这三个文件，将它们合并成一个DataFrame，按照奖牌总数降序排列

import pandas as pd
import numpy as np

#读取数据
data1=pd.read_csv('./data/各国奖牌预测_悲观.csv')
data2=pd.read_csv('./data/各国奖牌预测_乐观.csv')
data3=pd.read_csv('./data/各国奖牌预测_中等.csv')

#合并数据，以第一列为键，合并，Gold_x+Gold_y+Gold_z;Silver_x+Silver_y+Silver_z;Bronze_x+Bronze_y+Bronze_z
data=pd.merge(data1,data2,on='Country')
data=pd.merge(data,data3,on='Country')

#print(data)

#排序，按照奖牌总数降序排列
data['Gold']=(data['Gold_x']*0.5+data['Gold_y']*0.5+data['Gold'])/5
data['Gold']=data['Gold'].apply(lambda x:int(x))
data['Gold_x']=data['Gold_x']/2.5
data['Gold_x']=data['Gold_x'].apply(lambda x:int(x))

data['Gold_y']=data['Gold_y']/2.5
data['Gold_y']=data['Gold_y'].apply(lambda x:int(x))

data['Silver']=(data['Silver_x']*0.5+data['Silver_y']*0.5+data['Silver'])/5
data['Silver']=data['Silver'].apply(lambda x:int(x))
data['Silver_x']=data['Silver_x']/2.5
data['Silver_x']=data['Silver_x'].apply(lambda x:int(x))
data['Silver_y']=data['Silver_y']/2.5
data['Silver_y']=data['Silver_y'].apply(lambda x:int(x))


data['Bronze']=(data['Bronze_x']*0.5+data['Bronze_y']*0.5+data['Bronze'])/5
data['Bronze']=data['Bronze'].apply(lambda x:int(x))
data['Bronze_x']=data['Bronze_x']/2.5
data['Bronze_x']=data['Bronze_x'].apply(lambda x:int(x))
data['Bronze_y']=data['Bronze_y']/2.5
data['Bronze_y']=data['Bronze_y'].apply(lambda x:int(x))


data['Total']=data['Gold']+data['Silver']+data['Bronze']
data['Total']=data['Total'].apply(lambda x:int(x))

#由于悲观有时候会比乐观更接近实际情况，因此要对每个Gold_x,Gold_y,Gold进行重新排序，最大为Gold_y，最小为Gold_x,中间为Gold；Silver,Bronze同理
data['Gold_x'],data['Gold'],data['Gold_y']=np.sort(data[['Gold_x','Gold_y','Gold']].values,axis=1).T
data['Silver_x'],data['Silver'],data['Silver_y']=np.sort(data[['Silver_x','Silver_y','Silver']].values,axis=1).T
data['Bronze_x'],data['Bronze'],data['Bronze_y']=np.sort(data[['Bronze_x','Bronze_y','Bronze']].values,axis=1).T

data=data.sort_values(by='Total',ascending=False)
print(data)

#绘制一张图表，是USA的金牌、银牌、铜牌的预测值，悲观、乐观、中等三种情况，横坐标是金牌、银牌、铜牌，纵坐标是奖牌数
import matplotlib.pyplot as plt
import seaborn as sns

#筛选出USA的数据
usa_data=data[data['Country']=='USA']
#绘制图表
plt.figure(figsize=(10,6))
#金牌有三列，分别是Gold_x,Gold_y,Gold，代表乐观、悲观、中等情况，需要相邻绘制，银牌、铜牌同理
plt.bar(['Gold_pessimistic','Gold_neutral','Gold_optimistic'],usa_data[['Gold_x','Gold_y','Gold']].values[0],label='Gold')
plt.bar(['Silver_pessimistic','Silver_neutral','Silver_optimistic'],usa_data[['Silver_x','Silver_y','Silver']].values[0],label='Silver')
plt.bar(['Bronze_pessimistic','Bronze_neutral','Bronze_optimistic'],usa_data[['Bronze_x','Bronze_y','Bronze']].values[0],label='Bronze')
# #再加一列，表示总数，需要自己计算
# plt.bar(['Total_pessimistic','Total_optimistic','Total_neutral'],usa_data[['Gold_x','Gold_y','Gold']].values[0]+usa_data[['Silver_x','Silver_y','Silver']].values[0]+usa_data[['Bronze_x','Bronze_y','Bronze']].values[0],label='Total')

plt.title('USA Gold,Silver,Bronze Prediction')

plt.legend()

plt.show()


#重命名，_x,_y,改为_pessimistic_optimistic
data=data.rename(columns={'Gold_x':'Gold_pessimistic','Gold_y':'Gold_optimistic'})
data=data.rename(columns={'Silver_x':'Silver_pessimistic','Silver_y':'Silver_optimistic'})
data=data.rename(columns={'Bronze_x':'Bronze_pessimistic','Bronze_y':'Bronze_optimistic'})

#导出数据
data.to_csv('./data/各国奖牌预测.csv',index=False)
