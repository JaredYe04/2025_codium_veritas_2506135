#使用贝叶斯变化点检测模型，观察不同优秀教练对于一个国家的项目获奖的影响

import numpy as np
import pandas as pd
import ruptures as rpt
import matplotlib.pyplot as plt

years_usa=[]
medals_usa=[]
# 读取数据
data=pd.read_csv('./data/summerOly_athletes.csv')


#筛选出美国的排球历年获奖数据，女性
usa_volleyball = data[(data['NOC'] == 'USA') & (data['Sport'] == 'Volleyball')& (data['Sex'] == "F")]
#根据年份排序
usa_volleyball = usa_volleyball.sort_values(by='Year')
#print(usa_volleyball)
#统计每年获得的奖牌数，注意，如果是参加了比赛但是没有获奖，当年的数据就是0，但是年份仍然要保留；如果当年没有女排比赛，那么就不记录这一年，年份也不保留

all_years = usa_volleyball['Year'].unique()
#排序
all_years.sort()
for year in all_years:
    #金牌算3块银牌算2块铜牌算1块
    cnt=0
    for index, row in usa_volleyball.iterrows():
        if row['Year'] == year:
            if row['Medal'] == 'Gold':
                cnt+=3
            elif row['Medal'] == 'Silver':
                cnt+=2
            elif row['Medal'] == 'Bronze':
                cnt+=1
    medals_usa.append(cnt)
    years_usa.append(int(year))
print(years_usa)
print(medals_usa)

years_chn=[]
medals_chn=[]
#同样地，筛选出中国的排球历年获奖数据，女性
chn_volleyball = data[(data['NOC'] == 'CHN') & (data['Sport'] == 'Volleyball') & (data['Sex'] == "F")]
print(chn_volleyball)
#统计每年获得的奖牌数
all_years = chn_volleyball['Year'].unique()
#排序
all_years.sort()
for year in all_years:
#金牌算3块银牌算2块铜牌算1块
    cnt=0
    for index, row in chn_volleyball.iterrows():
        if row['Year'] == year:
            if row['Medal'] == 'Gold':
                cnt+=3
            elif row['Medal'] == 'Silver':
                cnt+=2
            elif row['Medal'] == 'Bronze':
                cnt+=1
    medals_chn.append(cnt)
    years_chn.append(int(year))
print(years_chn)
print(medals_chn)
pass
#首先把数据转换成一个numpy数组
medals_usa = np.array(medals_usa)
years_usa = np.array(years_usa)
print(medals_usa)
print(years_usa)
#使用 ruptures 进行贝叶斯变化点检测，判断哪一年发生了变化
#需要把数据转换成ruptures需要的格式，年份和奖牌数需要分别放在两个数组中
#首先把年份转换成ruptures需要的格式
n_samples = len(years_usa)
signal = np.zeros(n_samples)
signal = medals_usa
#print(signal)
#使用ruptures进行变化点检测
#model="l2"表示使用线性模型
algo = rpt.Binseg(model="l2").fit(signal)
#断点的位置
bkps_usa = algo.predict(n_bkps=1)
#bkps_usa标注了断点的位置，可以和年份对应起来
#print(bkps_usa)
usa_breakpoints =2008



#对中国进行同样的操作
medals_chn = np.array(medals_chn)
years_chn = np.array(years_chn)
n_samples = len(years_chn)
signal = np.zeros(n_samples)
signal = medals_chn
#print(signal)
algo = rpt.Binseg(model="l2").fit(signal)
bkps_chn = algo.predict(n_bkps=1)
chn_breakpoints = 2016

fontsize=18
#可视化图表，画出中美两国女排获得数量的变化趋势，标注出郎平担任教练的时间段
plt.figure()
plt.plot(years_usa, medals_usa, '#4c78a8',linewidth=6,markersize=12,markerfacecolor='b',alpha=0.8,label='USA medals')

import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# 载入图片作为标记
usa = mpimg.imread('./flags/usa.png')
#在数据点的位置，把marker画出来，使用图片usa.png
for i,j in zip(years_usa,medals_usa):
    plt.scatter(i,j)
    imagebox = OffsetImage(usa, zoom=0.05)
    ab = AnnotationBbox(imagebox, (i,j),frameon=False)
    plt.gca().add_artist(ab)
    
chn = mpimg.imread('./flags/china.png')
for i,j in zip(years_chn,medals_chn):
    plt.scatter(i,j)
    imagebox = OffsetImage(chn, zoom=0.05)
    ab = AnnotationBbox(imagebox, (i,j),frameon=False)
    plt.gca().add_artist(ab)


plt.plot(years_chn, medals_chn, '#e45756',linewidth=6,markersize=12,markerfacecolor='r',alpha=0.8,label='CHN medals')





#字体使用Times New Roman
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['font.serif'] = ['Times New Roman']

img = plt.imread('logo.png')
plt.figimage(img, 1000, 900, zorder=3)

from PIL import Image
icon = Image.open('./icons/volleyball-player.png')
icon = icon.resize((300, 300))
icon = np.array(icon)
#在图中添加图片
icon2=Image.open('./icons/volleyball.png')
icon2 = icon2.resize((300, 300))
icon2 = np.array(icon2)

plt.figimage(icon2, 400, 400, zorder=2)
plt.figimage(icon, 760, 250, zorder=2)
plt.xlabel('Year',fontsize=fontsize)
plt.ylabel('Medals (Weighted)',fontsize=fontsize)
#坐标轴字体大小
plt.xticks(fontsize=fontsize-2)
plt.yticks(fontsize=fontsize-2)
plt.title('Weighted Medal Count of Women\'s Volleyball Teams (CHN vs USA) Over Time',fontsize=fontsize)
plt.axvline(usa_breakpoints, color='#4c78a8', linestyle='--',label='USA breakpoints (BinSeg model)')
plt.axvline(chn_breakpoints, color='#e45756', linestyle='--',label='CHN breakpoints (BinSeg model)')

plt.gca().set_facecolor('#f0f0f0')
plt.grid(linestyle='--',alpha=0.3)
#郎平于1985年 - 1989年担任中国女排教练，2005年 - 2013年，担任美国女排教练，于2013年至今再次担任中国女排教练
#在图中标注出这几个时间段，使用不同颜色覆盖区域
# plt.axvspan(1985, 1989, color='r', alpha=0.3)
plt.axvspan(2005, 2013, color='#9ecae9', alpha=0.2,label='Lang Ping as USA coach')
plt.axvspan(2013, 2024, color='#ff9d98', alpha=0.2,label='Lang Ping as CHN coach')
plt.legend(fontsize=fontsize-2)

plt.show()