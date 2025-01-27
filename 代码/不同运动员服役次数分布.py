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

sns.kdeplot(result, shade=True)
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

