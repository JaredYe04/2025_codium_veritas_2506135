#如果某个强国的项目，连续几年奖牌数都很平缓，就考虑聘请名师来提高竞技水平。这里我们用CUSUM来分析哪些国家需要好教练。

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
#首先只取level=1,2,3的国家，它们是强国
# United States,1105,879,780,2764,1
# China,303,226,198,727,1
# Great Britain,299,339,343,981,2
# France,240,278,299,817,2
# Germany,220,225,259,704,3
# Italy,230,205,228,663,3
# Australia,182,192,226,600,3
# Japan,189,162,193,544,3
# Sweden,152,181,183,516,3
# Hungary,187,162,182,531,3
# Russia,147,126,150,423,3
countries=['United States','China','Great Britain','France','Germany','Italy','Australia','Japan','Sweden','Hungary','Russia']
nocs=['USA','CHN','GBR','FRA','GER','ITA','AUS','JPN','SWE','HUN','RUS']
data = pd.read_csv('./data/summerOly_athletes.csv')

#遍历这些国家的所有项目，每年的奖牌变化情况，如果连续三届奖牌数都很平缓，就考虑聘请名师来提高竞技水平

#首先获取所有项目
sports=data['Sport'].unique()
#然后获取所有年份
years=data['Year'].unique()

#然后遍历所有国家

medal_data={}
# for country,noc in zip(countries,nocs):
#     #获取该国家所有项目的奖牌变化情况
#     for sport in sports:
#         #获取该项目该国家的奖牌变化情况
#         sport_data=data[(data['NOC'] == noc) & (data['Sport'] == sport)]
#         #去除没有奖牌的记录
#         sport_data = sport_data[sport_data['Medal'] != 'No medal']
#         #统计每年获得的奖牌数
#         sport_total_medals = sport_data.groupby('Year').size()
#         sport_total_medals = sport_total_medals.reset_index()
#         sport_total_medals.columns = ['Year', 'Total']
#         #保存
#         if country not in medal_data:
#             medal_data[country]={}
#         medal_data[country][sport]=sport_total_medals
#         print(sport_total_medals)
        
# #如果在2016,2020,2024年，某个国家的某个项目的奖牌数都很平缓，就考虑聘请名师来提高竞技水平

# #保存medal_data
# import pickle
# with open('./data/medal_data.pkl','wb') as f:
#     pickle.dump(medal_data,f)
    
    
#读取medal_data
import pickle
with open('./data/medal_data.pkl','rb') as f:
    medal_data=pickle.load(f)


                
#然后我们使用CUSUM来分析哪些国家需要好教练
#首先我们需要计算每年的奖牌数的均值
means={}
for country in countries:
    for sport in sports:
        #获取该项目该国家的奖牌变化情况
        sport_total_medals=medal_data[country][sport]
        mean=sport_total_medals['Total'].mean()
        if country not in means:
            means[country]={}
        means[country][sport]=mean
        #print(country,sport,mean)
        
        
#print(means)
#然后我们计算CUSUM
#首先我们定义一个阈值
#然后我们计算CUSUM
cusums={}
for country in countries:
    cusums[country]={}
    for sport in sports:
        #获取该项目该国家的奖牌变化情况
        sport_total_medals=medal_data[country][sport]
        mean=means[country][sport]
        cusum=0
        cusum_list=[]
        for i in range(len(sport_total_medals)):
            #print(sport_total_medals)
            total=sport_total_medals['Total'].values[i]
            cusum+=total-mean
            #年份和CUSUM一起保存
            cusum_list.append((sport_total_medals['Year'].values[i],cusum))
        cusums[country][sport]=cusum_list
            

#一个国家奖牌获取的平缓程度，可以通过CUSUM来衡量，如果CUSUM一直为负，说明奖牌数一直低于平均值，需要好教练来提高竞技水平
#首先我们绘制CUSUM图，一个国家所有项目的CUSUM图
target_countries=['France','Sweden','Germany']
# target_countries=['United States','Sweden','China']
new_sports={}

min_sports={}
import math
for country in target_countries:
    
    #对于所选国家，项目应当筛选为，近3届CUSUM一直在递减的项目，注意是递减，而不是负值
    cusum_list=cusums[country][sport]
    years=[x[0] for x in cusum_list]
    cusum_list=[x[1] for x in cusum_list]
    filtered_sports=[]
    
    min_sport=None
    min_cusum=0
    for sport in sports:
        
        cusum_list=cusums[country][sport]
        #cusum_list的保存格式是[(year,cusum),...]
        years=[x[0] for x in cusum_list]
        cusum_list=[x[1] for x in cusum_list]
        descending=True
        #判断最后n个是否递减
        n=3
        if len(years)<5 or years[-1]!=2024:
            continue
        if len(cusum_list)<n:
            continue
        
        #最后4个点斜率越小，说明越平缓，越需要好教练
        if cusum_list[-1]-cusum_list[-(len(cusum_list)//4)]<0 and math.fabs(cusum_list[-1]-cusum_list[-(len(cusum_list)//4)])>min_cusum:
            min_sport=sport
            min_cusum=math.fabs(cusum_list[-1]-cusum_list[-(len(cusum_list)//4)])
            
        
        # for i in range(1,n):
        #     if cusum_list[-i]>cusum_list[-i-1]:
        #         descending=False
        #         break
        # if descending:
        filtered_sports.append(sport)
    new_sports[country]=filtered_sports
    min_sports[country]=min_sport
    
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['font.serif'] = ['Times New Roman']
fontsize=18
img_path='./flags/'
flags=['france.png','sweden.png','germany.png']

for country in target_countries:
    for sport in new_sports[country]:
        cusum_list=cusums[country][sport]
        #print(cusum_list)
        #cusum_list的保存格式是[(year,cusum),...]
        years=[x[0] for x in cusum_list]
        cusum_list=[x[1] for x in cusum_list]
        
        #print(cusum_list)
        
        
        if sport==min_sports[country]:
            plt.plot(years,cusum_list,label=sport,linewidth=5)
        else:
            plt.plot(years,cusum_list,label=sport,linewidth=3,alpha=0.3)
    plt.xlabel('Year',fontsize=fontsize)
    plt.ylabel('CUSUM',fontsize=fontsize)
    plt.title(country,fontsize=fontsize)
    
    # #在图中加入国旗
    # img = plt.imread(img_path+flags[target_countries.index(country)])
    # plt.figimage(img, 0, 0, zorder=3)
    from PIL import Image
    icon = Image.open(img_path+flags[target_countries.index(country)])
    icon = icon.resize((icon.size[0]//8, icon.size[1]//8))
    icon = np.array(icon)
    plt.figimage(icon, 570, 628, zorder=2)
    
    plt.gca().set_facecolor('#f0f0f0')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()

#改写以上代码，把三张图合并到一张图上
#fig,ax=plt.subplots(3,1,figsize=(10,15))
#times new roman


# for i in range(3):
#     country=target_countries[i]
#     print(min_sports[country])
#     for sport in new_sports[country]:
#         cusum_list=cusums[country][sport]
#         #cusum_list的保存格式是[(year,cusum),...]
#         years=[x[0] for x in cusum_list]
#         cusum_list=[x[1] for x in cusum_list]
        
#         # years=years[5:]
#         # cusum_list=cusum_list[5:]
#         #print(cusum_list)
#         if sport==min_sports[country]:
#             ax[i].plot(years,cusum_list,label=sport,linewidth=3)
#         else:
#             ax[i].plot(years,cusum_list,label=sport,linewidth=3,alpha=0.3)
#     #ax[i].set_xlabel('Year')
#     ax[i].set_ylabel('CUSUM')
#     ax[i].set_title(country)
#     ax[i].legend()
#     ax[i].set_facecolor('#f0f0f0')

