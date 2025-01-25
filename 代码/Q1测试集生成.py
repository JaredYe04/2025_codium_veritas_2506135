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

X_test=[]#测试集，我们根据预测的参数，给出X_test，然后投入模型，得出预测结果
#我们需要对每个国家每个项目的每名运动员进行预测


#乐观/中立/悲观参数
moods=['optimistic','neutral','pessimistic']

for mood in moods:
    print('正在处理'+mood+'情况')
    export_filename='./data/test_data_'+ mood+'.csv'
    #创建文件指针，用于写入数据，写入的数据是训练集
    f=open(export_filename,'w')
    #写入列名
    f.write('country,year,sport,is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg,Gold_prob,Silver_prob,Bronze_prob,No_medal_prob\n')

    country_idx=0
    for country in country_list:
        country_idx+=1
        print('正在处理第'+str(country_idx)+'个国家，代码为'+country,'共'+str(len(country_list))+'个国家')
        #首先确定国家要参加的项目，即每个项目，以及投入的人员数量
        terms=participant_count[participant_count['NOC']==country]['Sport'].values#参与的项目
        
        years=[2028]
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
                try:
                    
                    advantage_arg=float(advantage_arg)
                except:
                    advantage_arg=0

                #print(advantage_arg)
                if level[level['NOC']==code_2_name(country)]['level'].values.size==0:
                    level_arg=5
                else:
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
                
                
                ################################################################################################################
                #athletes=athlete_log[athlete_log['NOC']==country][athlete_log['Sport']==term][athlete_log['Year']==year]['Name'].values#参与的运动员
                #由于是预测，因此运动员是未知的，我们选取20%的上一届，2024年的运动员，加上80%的随机生成的新运动员，作为测试集
                last_athletes=athlete_log[athlete_log['NOC']==country][athlete_log['Sport']==term][athlete_log['Year']==year-4]['Name'].values
                if len(last_athletes)==0:
                    continue
                 #我们获取去年运动员所有的参数信息，然后进行排序，分别按照Gold_prob,Silver_prob,Bronze_prob,No_medal_prob排序
                last_athletes_args=athlete_args[athlete_args['Name'].isin(last_athletes)]
                last_athletes_args=last_athletes_args.sort_values(by=['Gold_prob','Silver_prob','Bronze_prob','No_medal_prob'],ascending=False)
                reserved_athletes=[]
                #对于乐观情况，只在前50%的运动员中选择总人数的20%，中立情况在所有人中选择总人数的20%，悲观情况在后50%的运动员中选择总人数的20%
                if mood=='optimistic':
                    reserved_athletes=last_athletes_args.head(int(len(last_athletes_args)/2)).sample(frac=0.4)['Name'].values
                elif mood=='neutral':
                    reserved_athletes=last_athletes_args.sample(frac=0.2)['Name'].values
                elif mood=='pessimistic':
                    reserved_athletes=last_athletes_args.tail(int(len(last_athletes_args)/2)).sample(frac=0.4)['Name'].values
                reserved_athletes_args=athlete_args[athlete_args['Name'].isin(reserved_athletes)]
                athletes=reserved_athletes_args.copy()
                #只保留必要的列
                athletes=athletes[['Gold_prob','Silver_prob','Bronze_prob','No_medal_prob']]
                #print(athletes)
                #转换成列表
                #print(athletes)
                #我们获取去年所有运动员这些获奖参数的平均值，作为今年新运动员的参数基准
                #print(last_athletes_args)
                #只筛选'Gold_prob','Silver_prob','Bronze_prob','No_medal_prob'，然后求均值
                last_athletes_args_mean=last_athletes_args[['Gold_prob','Silver_prob','Bronze_prob','No_medal_prob']].mean()
                #print(last_athletes_args_mean)

                #随机生成80%的新运动员，命名规则为ROC+term+year+index

                for i in range(int(len(reserved_athletes)*4)):

                    #除此之外，athlete_args里要生成一些参数，参数的基准为last_athletes_args_mean
                    #如果是乐观情况，那么我们在last_athletes_args_mean的基础上，每个参数都增加20%
                    #如果是中立情况，那么我们在last_athletes_args_mean的基础上，每个参数都不变
                    #如果是悲观情况，那么我们在last_athletes_args_mean的基础上，每个参数都减少20%
                    new_athlete_arg=last_athletes_args_mean
                    if mood=='optimistic':
                        new_athlete_arg=new_athlete_arg*1.2
                    elif mood=='pessimistic':
                        new_athlete_arg=new_athlete_arg*0.8
                    #加入20%随机扰动
                    new_athlete_arg=new_athlete_arg*(1+np.random.rand(4)*0.2)
                    #print(new_athlete_arg)
                    athletes.loc[len(athletes)]=new_athlete_arg
                    #print(athletes)
                    
                for athlete in athletes.values:
                    #('country,year,sport,is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg,Gold_prob,Silver_prob,Bronze_prob,No_medal_prob\n')
                    f.write(country+','+str(year)+','+term+','+','.join([str(x) for x in country_arg])+','+','.join([str(x) for x in athlete])+'\n')
                    
                
                    
                
                    
