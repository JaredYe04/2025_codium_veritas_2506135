#summerOly_athletes.csv

#分析每个国家每届奥运会中，新增的人数和离开的人数走势

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('./data/summerOly_athletes.csv')

# 以每个国家的每个项目为单位，统计每年新增的人数和离开的人数

#1896年为第一届奥运会，从下一届开始统计
years = data['Year'].unique()

#结果
result = []

for year in years:
    #本届数据
    current_data = data[data['Year'] == year]
    #上一届数据
    #上一届不一定是-4，因为有可能有一届奥运会没有举办
    last_year = year - 4
    # if last_year not in years:
    #     last_year = year - 2
    last_data = data[data['Year'] == last_year]
    #新增人数
    new_athletes = len(set(current_data['Name']) - set(last_data['Name']))
    #离开人数
    leave_athletes = len(set(last_data['Name']) - set(current_data['Name']))
    
    result.append([year,new_athletes,leave_athletes])
    
result = pd.DataFrame(result,columns=['Year','New','Leave'])


col_width=2.5
#绘制柱形图，增加的人数和离开的人数叠加显示，新增的人在左边，离开的人在右边
plt.figure(figsize=(10,6))
plt.bar(result['Year'],result['New'],label='New',width=col_width,color='#4c78a8')
#给出年份
plt.bar(result['Year'],result['Leave'],label='Leave',bottom=result['New'],width=col_width,color='#e45756')
plt.bar(result['Year']+col_width*0.7,np.abs(result['New']-result['Leave']),label='Variation',color=(result['New']-result['Leave']>0).map({True:'#439894',False:'#d67195'}),width=1)

plt.xlabel('Year',fontsize=20)
plt.ylabel('Number of Athletes',fontsize=20)
plt.title('Number of New and Leave Athletes in Each Year',fontsize=20)



#添加灰色bar用于标注
plt.bar(1916,8000,color='#bab0ac',width=col_width)
plt.text(1916,8000,'Cancelled due to WWI',ha='center',va='bottom',fontsize=14)
#添加灰色bar用于标注
plt.bar(1940,8000,color='#bab0ac',width=col_width)
plt.bar(1944,8000,color='#bab0ac',width=col_width)
#(1944,8000)处有注解，说明1944年奥运会取消了
plt.text(1940,8000,'Cancelled due to WWII',ha='center',va='bottom',fontsize=14)

#2020年因为疫情推迟到2021年，所以2020年的数据不准确
plt.text(2020,16000,'Affected by the epidemic',ha='center',va='bottom',fontsize=14)

#坐标的值，字体调大
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#修改背景样式
plt.style.use('ggplot')
#美化图表

#字体改成Times New Roman
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['font.serif'] = ['Times New Roman']


#坐标系内的背景色变成淡灰色，而不是外部的图表背景色
plt.gca().set_facecolor('#f0f0f0')


#网格线加粗，黑色，置于底层
plt.grid(linestyle='--', linewidth=0.5, color='black',zorder=-111)


#字体调大
plt.rcParams.update({'font.size': 16})

plt.legend()
plt.show()



pass