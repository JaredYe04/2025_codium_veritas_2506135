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
athlete_arg=pd.read_csv('./data/athlete_args.csv')



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
for country in country_list:
    #首先确定国家要参加的项目，即每个项目，以及投入的人员数量
    terms=participant_count[participant_count['NOC']==country]['Sport'].values.unique()#参与的项目
    years=participant_count[participant_count['NOC']==country]['Year'].values.unique()#参与的年份
    #编写数据集
    for term in terms:
        for year in years:
            #首先确定国家要参加的项目，即每个项目，以及投入的人员数量
            athletes=athlete_log[athlete_arg['NOC']==country][athlete_arg['Sport']==term][athlete_arg['Year']==year]['Name'].values#参与的运动员
    #athlete_log 