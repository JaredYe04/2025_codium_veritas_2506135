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


#分布拟合，使用核密度估计，绘制核密度图,查看分布情况
sns.kdeplot(result['Year'], shade=True)
plt.xlabel('Serve Years')
plt.ylabel('Density')
plt.title('Distribution of Serve Years')
plt.show()

#验证是否符合帕累托分布，绘制累积分布函数图
result = result.sort_values('Year')
result['cumsum'] = np.arange(len(result)) / len(result)
plt.plot(result['Year'], result['cumsum'])
plt.xlabel('Serve Years')
plt.ylabel('Cumulative Probability')
plt.title('Cumulative Distribution of Serve Years')

plt.show()


pass