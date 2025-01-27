#summerOly_athletes.csv

import pandas as pd
import numpy as np

# 读取数据
data = pd.read_csv('./data/summerOly_athletes.csv')

#groupby运动员名字，统计每个运动员参加的比赛次数
result = data.groupby('Name').size()
# 保存结果
result.to_csv('./data/athlete_serve_times_distribution.csv')

#描述统计
print(result.describe())

#分布拟合，使用核密度估计，绘制核密度图,查看分布情况
import matplotlib.pyplot as plt
import seaborn as sns

#分布拟合，使用核密度估计，绘制核密度图,查看分布情况
density=sns.kdeplot(result, shade=True,color='#4c78a8',linewidth=1.5)



#根据核密度估计，再画一条密度累积曲线，要覆盖面积
sns.kdeplot(result, cumulative=True,color='#439894',linewidth=2)

from scipy.signal import find_peaks
from scipy.stats import gaussian_kde
# 使用 gaussian_kde 进行核密度估计
kde = gaussian_kde(result, bw_method=100)  # 可以调整bw_method以改变平滑度
x_vals = np.linspace(result.min(), result.max(), 1000)  # 生成更多的x值
y_vals = kde(x_vals)  # 计算相应的y值
# 找到峰值位置
peaks, _ = find_peaks(y_vals)


plt.scatter(0.82, 0.82, color='#e55756', marker='*', s=200, zorder=5)
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#x轴范围改为0-10
plt.xlim(0, 10)

#网格线加粗，黑色
plt.grid(linestyle='--', linewidth=0.5, color='black')


#坐标系内的背景色变成淡灰色，而不是外部的图表背景色
plt.gca().set_facecolor('#f0f0f0')

#添加均值线
plt.axvline(result.mean(), linestyle='--', linewidth=2,color='#79706e')

#图例
plt.legend(['Density','Cumulative Density','Peak','Mean'],fontsize=17)



plt.xlabel('Serve Times')
plt.ylabel('Density')
plt.title('Distribution of Serve Times')
plt.show()

# count    129992.000000
# mean          1.942927
# std           1.953005
# min           1.000000
# 25%           1.000000
# 50%           1.000000
# 75%           2.000000
# max          76.000000

