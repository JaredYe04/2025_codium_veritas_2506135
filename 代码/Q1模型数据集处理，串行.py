import warnings

# 禁用特定的警告
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)


#最终要得到的表格列头是，NOC,Year,Golds,Medals
# 主要模型：逻辑回归

# 自变量X：
# （国家因素）
# 1.是否为东道主
# 2.奖牌预期增量数（注意是增量数）*预期投入人员数量增量数（注意是增量数）
# 3.某项目优势系数
# 4.国家level（需要对level排序）
# 5.某项目奖牌预期数量/某项目预期投入人员数量
# p.s.对于小国家，变量2要给予相应奖励权重，即，有可能随着比赛奖项扩招，而小国家出现“黑马”的情况
# （运动员因素）
# 1.金牌概率
# 2.银牌概率
# 3.铜牌概率
# 4.无牌概率

# 因变量y：选用两套，一套是金牌数，一套是奖牌数。


#预测的最大单位是国家，因此需要对国家进行分组，然后对每个国家进行预测
#首先对国家进行分组，然后对每个国家进行预测

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 运动员记录，用于确定选了哪些运动员（以前）
athlete_log = pd.read_csv('./data/summerOly_athletes.csv')#运动员往年比赛记录，往年运动员的列表是固定的，因此可以用来训练，未来的需要自己生成

#东道主数据
host = pd.read_csv('./data/hosts.csv')

#NOC映射数据
NOCmap=pd.read_csv('./data/noc_region.csv')

#奖牌预期增量数
medal_trend = pd.read_csv('./data/predict_medal_trend.csv')

#预期投入人员数量增量数
athlete_trend = pd.read_csv('./data/predict_athlete_number_variation.csv')

#某项目优势系数
advantage = pd.read_csv('./data/country_adeptness.csv')

#国家level
level = pd.read_csv('./data/country_level.csv')

#某项目奖牌预期数量
medal_count = pd.read_csv('./data/predict_medal_counts.csv')

#某项目预期投入人员数量
participant_count = pd.read_csv('./data/predict_participants.csv')

#运动员因素
athlete_args=pd.read_csv('./data/athlete_args.csv')



export_filename='./data/train_data.csv'
#创建文件指针，用于写入数据，写入的数据是训练集
f=open(export_filename,'w')
#写入列名
f.write('is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg,Gold_prob,Silver_prob,Bronze_prob,No_medal_prob,Gold,Silver,Bronze\n')

#一个个国家进行预测
country_list = athlete_log['NOC'].unique()#三位代码

def code_2_name(code):
    result=NOCmap[NOCmap['NOC'] == code]['Country'].values[0]
    if result is None:
        print('无法映射'+code)
        return '未知'
    return result

def name_2_code(name):
    result=NOCmap[NOCmap['Country'] == name]['NOC'].values[0]
    if result is None:
        print('无法映射'+name)
        return '未知'
    return result

#我们最终是要训练一个，把一个运动员的一场比赛丢进去，就可以得出金牌概率以及奖牌概率的模型
#因此我们需要收集所有国家所有运动员比赛的数据，然后进行训练，得出一个模型
#然后我们使用预测的数据，投入模型，进行预测

X_train=[]#训练集，一条数据包含了一个运动员在某场比赛的参数，运动员自身的参数，国家背景相关的参数
y_train=[]#训练集，一条数据包含了一个运动员在某场比赛的奖牌情况

country_idx=0
for country in country_list:
    country_idx+=1
    print('正在处理第'+str(country_idx)+'个国家，代码为'+country,'共'+str(len(country_list))+'个国家')
    #首先确定国家要参加的项目，即每个项目，以及投入的人员数量
    terms=participant_count[participant_count['NOC']==country]['Sport'].values#参与的项目
    
    years=participant_count[participant_count['NOC']==country]['Year'].values#参与的年份
    #去重
    terms=list(set(terms))
    years=list(set(years))
    this_noc=code_2_name(country)
    #print(terms)
    #print(years)
    #编写数据集
    term_idx=0
    for term in terms:
        term_idx+=1
        print('正在处理第'+str(term_idx)+'个项目，共'+str(len(terms))+'个项目')
        for year in years:
            athletes=athlete_log[athlete_log['NOC']==country][athlete_log['Sport']==term][athlete_log['Year']==year]['Name'].values#参与的运动员
            #print(athletes)
            for athlete in athletes:
                #确定运动员的参数
                athlete_arg=athlete_args[athlete_args['Name']==athlete]
                #只取Gold_prob,Silver_prob,Bronze_prob,No_medal_prob
                athlete_arg=athlete_arg[['Gold_prob','Silver_prob','Bronze_prob','No_medal_prob']]
                
                #确定国家的参数
                host_arg=host[host['Year']==year]
                #print(host_arg)
                host_noc=name_2_code(host_arg['Host'].values[0])
                #print(host_noc)
                is_host_arg=0.0#变量1
                if this_noc==host_noc:
                    is_host_arg=1.0
                #print(is_host_arg)
                #print(str(year))
                medal_trend_arg=medal_trend[medal_trend['Sport']==term][str(year)]#这个数据集的列名是年份，因此可以直接用年份来索引
                if medal_trend_arg.values.size==0:
                    medal_trend_arg=0
                #medal_trend_arg=float(medal_trend_arg)
                #print(medal_trend_arg)
                athlete_trend_arg=athlete_trend[athlete_trend['Sport']==term][athlete_trend['Year']==year][athlete_trend['NOC']==country]['New']
                athlete_trend_arg=float(athlete_trend_arg)
                #print(athlete_trend_arg)
                dmedel_dathlete_arg=0
                #print(medal_trend_arg)
                try:
                    dmedel_dathlete_arg=medal_trend_arg/athlete_trend_arg#变量2
                except:
                    dmedel_dathlete_arg=0#如果出现0除错误，赋值为0
                    
                dmedel_dathlete_arg=float(dmedel_dathlete_arg)
                
                advantage_arg=advantage[advantage['Sport']==term][advantage['NOC']==country]['Adeptness']#变量3
                advantage_arg=float(advantage_arg)

                #print(advantage_arg)
                level_arg=level[level['NOC']==code_2_name(country)]['level'].values[0]#变量4，这个数据集的列名是国家名，因此需要先转换
                
                level_arg=float(level_arg)
                #print(level_arg)
                if level_arg==5:
                    dmedel_dathlete_arg=dmedel_dathlete_arg*2#对于level=5的国家，给予奖励权重
                
                medal_count_arg=medal_count[medal_count['Sport']==term][str(year)]
                if medal_count_arg.values.size==0:
                    medal_count_arg=0
                medal_count_arg=float(medal_count_arg)
                #print(medal_count_arg)
                participant_count_arg=participant_count[participant_count['Sport']==term][participant_count['Year']==year][participant_count['NOC']==country]['Athletes']
                if participant_count_arg.values.size==0:
                    participant_count_arg=0
                participant_count_arg=float(participant_count_arg)
                #print(participant_count_arg)
                
                win_likely_arg=0
                try:
                    win_likely_arg=medal_count_arg/participant_count_arg#变量5
                except:
                    win_likely_arg=0#如果出现0除错误，赋值为0
                    
                win_likely_arg=float(win_likely_arg)
                
                #is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg#国家背景参数
                #把所有参数转换成数值，再拼接成列表
                country_arg=pd.Series([is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg])
                
                #转换成pd.Series
                athlete_arg=pd.Series(athlete_arg.values[0])
                arg=pd.concat([country_arg,athlete_arg],axis=0)
                # print(country_arg)
                # print(athlete_arg)
                # print(arg)
                #把arg加入到X_train中
                
                
                #y是一个向量，第一个元素是期望的金牌数，第二个元素是期望的银牌数，第三个元素是期望的铜牌数
                #确定y
                y=athlete_log[athlete_log['NOC']==country][athlete_log['Sport']==term][athlete_log['Year']==year][athlete_log['Name']==athlete]['Medal'].values
                #这是一个序列， 里面包含了['No medal', 'Gold', 'Silver', 'Bronze']四个元素，把它转换为一个三元素的向量，分别是金牌数，银牌数，铜牌数
                gold=0
                silver=0
                bronze=0
                for i in y:
                    if i=='Gold':
                        gold+=1
                    elif i=='Silver':
                        silver+=1
                    elif i=='Bronze':
                        bronze+=1
                y=[gold,silver,bronze]
                X_train.append(arg)
                y_train.append(y)
                #向文件中写入数据
                f.write(','.join([str(i) for i in arg]))
                f.write(',')
                f.write(','.join([str(i) for i in y]))
                f.write('\n')
                
                
                
# #保存数据集
# X_train=pd.DataFrame(X_train)
# y_train=pd.DataFrame(y_train)
# X_train.to_csv('./data/X_train.csv')
# y_train.to_csv('./data/y_train.csv')
                
#    #athlete_log 