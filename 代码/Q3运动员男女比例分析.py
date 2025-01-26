#分析历届奥运会男女运动员比例，以及获奖运动员男女比例
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 读取数据
data = pd.read_csv('./data/summerOly_athletes.csv')

# 统计每年男女运动员比例
# 总运动员数
total_athletes = data.groupby('Year').size()

with_award=''
# 男运动员数
male_athletes = data[data["Sex"] == "M"].groupby('Year').size()

# 女运动员数
female_athletes = data[data["Sex"] == "F"].groupby('Year').size()





with_award=' (with Award)'
male_athletes = data[(data["Sex"] == "M")][(data["Medal"] == "No medal")].groupby('Year').size()
female_athletes = data[(data["Sex"] == "F") ][ (data["Medal"] == "No medal")].groupby('Year').size()





ratio = male_athletes / total_athletes
print(ratio)

#绘制历届奥运会男女运动员数量柱形图，坐标轴在左侧表示数量，并在此基础上绘制性别比的折线图，坐标轴在右边
# 设置柱子的宽度
bar_width = 1.8  # 控制每个柱子的宽度

# 创建男生和女生的柱子位置


fontsize=15

# 创建图形和主坐标轴
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制男生柱状图
ax1.bar(male_athletes.index, male_athletes.values, color='#4c78a8', width=bar_width, label='Male Athletes',alpha=0.8)

# 绘制女生柱状图
ax1.bar(female_athletes.index + bar_width, female_athletes.values, color='#d67195', width=bar_width, label='Female Athletes',alpha=0.8)

# 设置x轴标签
ax1.set_xticks(male_athletes.index + bar_width / 2)  # 将x轴的标签放在两个柱子中间
ax1.set_xticklabels(male_athletes.index,rotation=45,fontsize=fontsize-3)

# 创建第二个y轴（右侧y轴）
ax2 = ax1.twinx()

# 绘制性别比率的折线图，参照右侧y轴，标出数值
ax2.plot(ratio.index, ratio.values, color='#e45756', marker='*', label='Ratio of Gender', linestyle='--', linewidth=2, markersize=10)


# 设置y轴标签
ax1.set_ylabel('Number of Athletes',fontsize=fontsize)
ax2.set_ylabel('Gender Ratio',fontsize=fontsize)

# 添加图例
ax1.legend(loc='upper left',fontsize=fontsize)
ax2.legend(loc='upper right',fontsize=fontsize)


ax1.set_xlabel('Year',fontsize=fontsize)

#设置标题为，历届奥运会运动员性别分布
#plt.title(f'Gender Distribution of Athletes{with_award}',fontsize=fontsize)
#times new roman
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False
plt.grid(True)
ax1.set_facecolor('#f0f0f0')
ax2.set_facecolor('#f0f0f0')
#字体大小
plt.show()