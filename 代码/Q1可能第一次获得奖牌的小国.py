#如果某种比赛的奖牌数有上升趋势，并且尚未获得奖牌的国家，曾参与过该种比赛
#那么该国家有可能在未来的比赛中获得奖牌

#首先获取所有奖牌数有上升趋势的比赛项目


import pandas as pd
import numpy as np

#读取数据
data = pd.read_csv('./data/predict_medal_trend.csv')

trending_sports = data[data['2028'] > 0]
trending_sports = trending_sports[['Sport','2028']]
print(trending_sports)

#获取所有尚未获得奖牌的国家
data = pd.read_csv('./data/summerOly_athletes.csv')
countries = data['NOC'].unique()

sports=data['Sport'].unique()
# #如果有一个国家的所有运动员参与的比赛，都是No medal,就说明从未获得过奖牌
# no_medal_countries = []
# idx=0
# for country in countries:
#     idx+=1
#     print(idx,"/",len(countries))
#     has_medal = False
#     for sport in sports:
#         medals=data[(data['NOC'] == country) & (data['Sport'] == sport)]['Medal']
#         if medals is not None and ('Gold' in medals.values or 'Silver' in medals.values or 'Bronze' in medals.values):
#             has_medal = True
#             break
#     if not has_medal:
        
#         taken_part_sports = data[data['NOC'] == country]['Sport'].unique()
#         #统计每个项目的参与人次
#         taken_part_info = []
#         for sport in taken_part_sports:
#             times=len(data[(data['NOC'] == country) & (data['Sport'] == sport)])
#             taken_part_info.append((sport,times))
        
#         no_medal_countries.append((country,taken_part_info))
#         print((country,taken_part_info))

# print(no_medal_countries)
# #保存结果
# result = pd.DataFrame(no_medal_countries,columns=['NOC','Sport'])
# result.to_csv('./data/no_medal_countries.csv',index=False)

# #读取数据
# no_medal_countries = pd.read_csv('./data/no_medal_countries.csv')

# print(no_medal_countries)

# #计算每个国家首次获奖的可能性

# probs = []
# for index, row in no_medal_countries.iterrows():
#     country = row['NOC']
#     sports = row['Sport']
#     #sports是一个字符串，需要转换为列表
#     sports = eval(sports)
#     prob = 0
#     for (sport,times) in sports:
#         if sport in trending_sports['Sport'].values:
#             prob += trending_sports[trending_sports['Sport'] == sport]['2028'].values[0]*times
#     probs.append((country,prob))
#     print(country,prob)

# #排序，按照prob降序排列
# probs = sorted(probs,key=lambda x:x[1],reverse=True)
# result = pd.DataFrame(probs,columns=['NOC','Prob'])
# result.to_csv('./data/first_medal_prob.csv',index=False)
# print(result)


ranking=pd.read_csv('./data/first_medal_prob.csv')

#取前15个国家
ranking = ranking.head(15)

#绘制柱形图
import matplotlib.pyplot as plt


#字体为Times New Roman
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['font.serif'] = ['Times New Roman']
#设置背景色


plt.figure(figsize=(10,6))
plt.grid(linestyle='--',alpha=0.2)
plt.bar(ranking['NOC'],ranking['Prob'],color='#4c78a8')

# #给排在前三名的柱子换个颜色
# plt.bar(ranking['NOC'].iloc[0],ranking['Prob'].iloc[0],color='#54a24b')
# plt.bar(ranking['NOC'].iloc[1],ranking['Prob'].iloc[1],color='#54a24b')
# plt.bar(ranking['NOC'].iloc[2],ranking['Prob'].iloc[2],color='#54a24b')


#添加国旗
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

#国旗文件夹
flag_folder = './flags/'

#国旗文件名
flags=['sierra-leone.png', 'antigua-and-barbuda.png', 'papua-new-guinea.png', 'liberia.png', 
 'myanmar.png', 'madagascar.png', 'nicaragua.png', 'samoa.png', 'seychelles.png', 
 'south-africa.png', 'el-salvador.png', 'nepal.png', 'republic-of-the-congo.png', 
 'gambia.png', 'lesotho.png']
country_names=['Sierra Leone', 'Antigua and Barbuda', 'Papua New Guinea', 'Liberia', 
 'Myanmar', 'Madagascar', 'Nicaragua', 'Samoa', 'Seychelles', 
 'South Africa', 'El Salvador', 'Nepal', 'Congo Republic', 
 'Gambia', 'Lesotho']
colors=['#e45756','#f58518','#f2cf5b','#54a24b'
        ,'#439894','#4c78a8','#b279a2','#d6a5c9',
        '#9ecae9','#83bcb6','#88327a','#ffbf79',
        '#d8b5a5','#ff9d98','#bab0ac'
        ]
for i in range(15):
    flag = mpimg.imread(flag_folder+flags[i])
    imagebox = OffsetImage(flag, zoom=0.092)
    ab = AnnotationBbox(imagebox, (i, ranking['Prob'].iloc[i]-1),frameon=False)
    plt.gca().add_artist(ab)
    #在柱状图上叠加显示国家名，并且竖排展示
    plt.text(i,ranking['Prob'].iloc[i]/4,country_names[i],rotation=90,ha='center',va='bottom',fontsize=23,fontweight='bold')
    plt.bar(ranking['NOC'].iloc[i],ranking['Prob'].iloc[i],color=colors[i])
#再增加一个logo.png贴图，放右上角
img = plt.imread('logo.png')
plt.figimage(img, 1800, 900, zorder=3)
plt.xticks(rotation=45)
plt.xlabel('Country',fontsize=20)
plt.ylabel('ξ',fontsize=20,rotation=0)
#y标签也应该竖直排列，因此设置rotation

plt.gca().set_facecolor('#f0f0f0')

plt.title('The Probability of First Medal in 2028',fontsize=12)
plt.show()
