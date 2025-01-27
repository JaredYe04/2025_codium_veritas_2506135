#summerOly_athletes.csv

import pandas as pd
import numpy as np

# # 读取数据
# data = pd.read_csv('./data/summerOly_athletes.csv')

# #groupby运动员名字，统计每个运动员参加的比赛年份跨度
# result = data.groupby('Name').agg({'Year': lambda x: x.max() - x.min() + 1})
# # 保存结果
# result.to_csv('./data/athlete_serve_distribution.csv')


#绘制分布图
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据

data = pd.read_csv('./data/summerOly_athletes.csv')

# #groupby运动员名字，统计每个运动员参加的比赛年份跨度
result = data.groupby('Name').agg({'Year': lambda x: x.max() - x.min() + 1})

#年限超过40可能是异常值，将其删除
result = result[result['Year'] <= 40]

# 描述统计
print(result.describe())
#字体改成Times New Roman
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)


#网格线加粗，黑色
plt.grid(linestyle='--', linewidth=0.5, color='black')


#坐标系内的背景色变成淡灰色，而不是外部的图表背景色
plt.gca().set_facecolor('#f0f0f0')


#分布拟合，使用核密度估计，绘制核密度图,查看分布情况
density=sns.kdeplot(result['Year'], shade=True,color='#4c78a8',linewidth=1.5)



#根据核密度估计，再画一条密度累积曲线，要覆盖面积
sns.kdeplot(result['Year'], cumulative=True,color='#439894',linewidth=2)

from scipy.signal import find_peaks
from scipy.stats import gaussian_kde
# 使用 gaussian_kde 进行核密度估计
kde = gaussian_kde(result['Year'], bw_method=0.5)  # 可以调整bw_method以改变平滑度
x_vals = np.linspace(result['Year'].min(), result['Year'].max(), 1000)  # 生成更多的x值
y_vals = kde(x_vals)  # 计算相应的y值
# 找到峰值位置
peaks, _ = find_peaks(y_vals)

# 在每个峰值位置绘制星号
for peak in peaks:
    plt.scatter(1, 0.78, color='#e55756', marker='*', s=200, zorder=5)


#宽度变大
plt.xlim(0, 20)

#添加均值线
plt.axvline(result['Year'].mean(), linestyle='--', linewidth=2,color='#79706e')

#图例
plt.legend(['Density','Cumulative Density','Peak','Mean'],fontsize=17)


plt.xlabel('Serve Years',fontsize=17)
plt.ylabel('Density',fontsize=17)
plt.title('Distribution of Serve Years',fontsize=20)
plt.show()


# #验证是否符合帕累托分布，绘制累积分布函数图
# result = result.sort_values('Year')
# result['cumsum'] = np.arange(len(result)) / len(result)
# plt.plot(result['Year'], result['cumsum'])
# plt.xlabel('Serve Years')
# plt.ylabel('Cumulative Probability')
# plt.title('Cumulative Distribution of Serve Years')


# plt.show()


pass