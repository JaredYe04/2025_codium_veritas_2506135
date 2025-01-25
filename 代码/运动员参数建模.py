#summerOly_athletes.csv
#对运动员在职业生涯中的金牌概率，银牌概率，铜牌概率，无奖牌概率进行统计

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('./data/summerOly_athletes.csv')

# #groupby运动员名字，统计每个运动员金牌，银牌，铜牌，无奖牌的次数
result = data.groupby('Name')['Medal'].value_counts().unstack().fillna(0)
print(result)
#计算金牌概率，银牌概率，铜牌概率，无奖牌概率
result['Gold_prob'] = result['Gold'] / result.sum(axis=1)
result['Silver_prob'] = result['Silver'] / result.sum(axis=1)
result['Bronze_prob'] = result['Bronze'] / result.sum(axis=1)
result['No_medal_prob'] = result['No medal'] / result.sum(axis=1)
# 保存结果
result.to_csv('./data/athlete_args.csv')