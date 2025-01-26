import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
YEAR_THRES = 1800


# 设置全局变量，支持自定义国家名和运动项目名

COUNTRY = 'China'  # 国家名
NOC='CHN'
SPORT = 'Table Tennis'  # 运动项目名
DISCIPLINE = 'Table Tennis'


# COUNTRY = 'Jamaica'  # 国家名
# NOC='JAM'
# SPORT = 'Athletics'  # 运动项目名
# DISCIPLINE = 'Athletics'

# #新西兰赛艇
# COUNTRY = 'New Zealand'  # 国家名
# NOC='NZL'
# SPORT = 'Rowing'  # 运动项目名
# DISCIPLINE = 'Rowing'



# 读取奖牌数据
data = pd.read_csv('./data/summerOly_medal_counts.csv')

# 筛选年份，选择YEAR_THRES年之后的数据
data = data[data['Year'] > YEAR_THRES]


total_medals = data[data['NOC'] == COUNTRY][['Year', 'Total']]

# 删除第一列索引

total_medals = total_medals.reset_index(drop=True)

# 读取运动员数据
data = pd.read_csv('./data/summerOly_athletes.csv')

# 筛选出指定国家和指定运动项目的奖牌数据
sport_medals = data[(data['NOC'] == NOC) & (data['Sport'] == SPORT) & (data['Year'] > YEAR_THRES)]

# 去除没有奖牌的记录
sport_medals = sport_medals[sport_medals['Medal'] != 'No medal']

# 统计每年获得的奖牌数
sport_total_medals = sport_medals.groupby('Year').size()
sport_total_medals = sport_total_medals.reset_index()
sport_total_medals.columns = ['Year', 'Total']

# 读取项目数据
data = pd.read_csv('./data/summerOly_programs.csv')

# 筛选出指定运动项目的所有数据
sport_data = data[data['Discipline'] == DISCIPLINE][data['Sport'] == SPORT]

# 去除不需要的列
sport_data = sport_data.drop(columns=['Discipline', 'Code', 'Sports Governing Body'])

# 统计每年指定运动项目的奖牌数
award_counts = pd.DataFrame(columns=['Year', 'Total'])
for year in sport_data.columns[1:]:
    award_counts.loc[len(award_counts)] = [year, sport_data[year].sum()]

# 转换年份格式并筛选YEAR_THRES年后的数据
print (award_counts)
award_counts['Year'] = award_counts['Year'].astype(int)
award_counts = award_counts[award_counts['Year'] > YEAR_THRES]
print (award_counts)
# 合并数据
result = pd.merge(total_medals, sport_total_medals, on='Year')
result = pd.merge(result, award_counts, on='Year')
result.columns = ['Year', 'Total Medals', f'{SPORT} Medals', f'World {SPORT} Medals']
# print(result)
# # 导出结果到CSV
# result.to_csv(f'./data/{SPORT.lower().replace(" ", "_")}_relationship.csv', index=False)

# 计算斯皮尔曼相关系数
#应当去除year列
result=result.drop(columns=['Year'])
correlation = result.corr(method='spearman')
print(correlation)

# 绘制热力图
plt.figure(figsize=(10, 6))
sns.heatmap(correlation, annot=True,cmap='coolwarm')
#颜色由浅变深表示相关性由低到高，最低为-1，红色，最高为1，绿色，0为白色
#cmap='coolwarm'表示颜色从冷到热


plt.title(f'{COUNTRY} Medal Correlation Heatmap')
plt.show()

# 转换相关性数据格式为 Type1 Type2 Correlation
correlation = correlation.reset_index()
correlation = pd.melt(correlation, id_vars='index')
correlation.columns = ['Type1', 'Type2', 'Correlation']

# 导出相关性数据
correlation.to_csv(f'./data/correlations/{COUNTRY.lower()}_correlation.csv', index=False)
