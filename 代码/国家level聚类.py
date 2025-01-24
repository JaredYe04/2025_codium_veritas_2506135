#写一个k-means聚类算法，自变量为某国家总共在奥运会上获得的铜牌，银牌，金牌数，总数因变量为该国家的level（1-5）
#导入数据集
from sklearn.cluster import KMeans
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

#导入数据集
data = pd.read_csv('./data/summerOly_medal_counts.csv')
data = data.dropna()

#Year<1992的数据不要
data = data[data['Year']>=1992]


#首先对数据进行求和，里面包含了历届奥运会的数据，我们需要groupby国家，然后对铜牌列，银牌列，金牌列，总数进行求和
data = data.groupby('NOC').sum()



#只需要Gold	Silver	Bronze	Total这四列
data = data[['Gold', 'Silver', 'Bronze', 'Total']]


#创建模型
kmeans = KMeans(n_clusters=5)
#训练模型
kmeans.fit(data)
#预测
prediction = kmeans.predict(data)
#输出
data['level'] = prediction
print(data)

#画图，画3D的聚类图，x轴为铜牌数，y轴为银牌数，z轴为金牌数，不同level的国家用不同颜色表示
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data['Bronze'], data['Silver'], data['Gold'], c=prediction)


#每个散点要显示国家名，这里只显示总奖牌数前10的国家
top10 = data.sort_values(by='Total', ascending=False).head(10)

#对前十名国家，要从坐标轴三个面上，作三条垂直于平面，并经过散点的黑色直线，例如散点(1,2,3)，则要画三条线，分别是(1,0,0),(0,2,0),(0,0,3)，经过(1,2,3)
idx=0
for index, row in top10.iterrows():
    #画一条垂直于Silver和Bronze平面的线，经过散点(row['Bronze'], row['Silver'], 0)
    #ax.plot([row['Bronze'], row['Bronze']], [row['Silver'], row['Silver']], [0, row['Gold']], color='black')
   
    #在该国家坐标轴周围偏20%的位置显示国家名，并用线连接国家名与散点
    #交错显示，如果index%2==0，则偏转20%，否则偏转-20%
    if idx%2==0:        
        ax.text(row['Bronze']*1.2, row['Silver'], row['Gold']*1.2, index)
        ax.plot([row['Bronze'], row['Bronze']*1.2], [row['Silver'], row['Silver']], [row['Gold'], row['Gold']*1.2], color='gray')
    else:
        ax.text(row['Bronze']*0.8, row['Silver'], row['Gold']*1.2, index)
        ax.plot([row['Bronze'], row['Bronze']*0.8], [row['Silver'], row['Silver']], [row['Gold'], row['Gold']*1.2], color='gray')
    idx+=1

    
    # #画一条垂直于Gold和Bronze平面的线，经过散点(row['Bronze'], 0, row['Gold'])
    # ax.plot([row['Bronze'], row['Bronze']], [0, row['Silver']], [row['Gold'], row['Gold']], color='black')
    # #画一条垂直于Gold和Silver平面的线，经过散点(0, row['Silver'], row['Gold'])
    # ax.plot([0, row['Bronze']], [row['Silver'], row['Silver']], [row['Gold'], row['Gold']], color='black')
#给图加上坐标轴标签
ax.set_xlabel('Bronze')
ax.set_ylabel('Silver')
ax.set_zlabel('Gold')

#给图加上标题，标题大意为：奥运会参赛国家聚类图
plt.title('Olympic countries clustering (1992-2024)')

#图片空间要有3d网格
ax.grid(True)

#图片背景颜色选用好看的淡橙色
ax.set_facecolor('peachpuff')

#图片尺寸应最大化，防止标签重叠
fig.set_size_inches(18.5, 10.5)
plt.show()


# data.to_csv('./data/country_level_.csv')