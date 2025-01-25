#导入金牌、银牌、铜牌三个pkl文件,并预测
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#导入数据，测试集有三份，乐观、中等、悲观
datas=[]
datas.append(pd.read_csv('./data/test_data_optimistic.csv'))
datas.append(pd.read_csv('./data/test_data_neutral.csv'))
datas.append(pd.read_csv('./data/test_data_pessimistic.csv'))

#导入模型
models=[]
models.append(joblib.load('./models/Gold.pkl'))
models.append(joblib.load('./models/Silver.pkl'))
models.append(joblib.load('./models/Bronze.pkl'))
mode=['乐观','中等','悲观']
#预测
for i in range(3):
    result={}
    #以国家代码为键，值为一个子哈希表，子表中有三个值，分别是Gold,Silver,Bronze
    #以下是数据示例
# country,year,sport,is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg,Gold_prob,Silver_prob,Bronze_prob,No_medal_prob
# CHN,2028,Weightlifting,0.0,0.6549771537166285,0.0974930362116991,3.0,1.4583845248836282,1.0,0.0,0.0,0.0
# CHN,2028,Weightlifting,0.0,0.6549771537166285,0.0974930362116991,3.0,1.4583845248836282,1.1490649390300882,0.0,0.0,0.08076753629702706
# CHN,2028,Weightlifting,0.0,0.6549771537166285,0.0974930362116991,3.0,1.4583845248836282,1.1719569818756443,0.0,0.0,0.08799395973968004
    #从is_host_arg开始，到No_medal_prob结束，是特征值；开头的country是国家代码，是键
    
    #首先获取国家列表
    countries=datas[i]['country'].unique()
    for country in countries:
        #获取该国家的数据
        data=datas[i][datas[i]['country']==country]
        #将特征值提取出来
        X=data.iloc[:,3:]
        
        #处理异常值
        #nan值处理,填充为0
        X.fillna(0,inplace=True)
        #对于特征进行归一化处理
        from sklearn.preprocessing import StandardScaler
        scaler=StandardScaler()
        X=scaler.fit_transform(X)


        #使用多项式特征生成器
        from sklearn.preprocessing import PolynomialFeatures
        poly=PolynomialFeatures(degree=2)
        
        X=poly.fit_transform(X)

        result[country]={}
        result[country]['Gold']=models[0].predict(X).sum()
        result[country]['Gold']=int(result[country]['Gold'])
        result[country]['Silver']=models[1].predict(X).sum()
        result[country]['Silver']=int(result[country]['Silver'])
        result[country]['Bronze']=models[2].predict(X).sum()
        result[country]['Bronze']=int(result[country]['Bronze'])
        print(country,result[country])
    
    
    #将结果写入文件
    with open('./data/_各国奖牌预测_'+mode[i]+'.csv','w') as f:
        #result转换为dataframe
        result=pd.DataFrame(result).T
        #print(result)
        #列名
        result.columns=['Gold','Silver','Bronze']
        result.to_csv(f)
        