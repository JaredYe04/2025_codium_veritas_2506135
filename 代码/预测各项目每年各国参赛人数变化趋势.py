#n_participants.csv

#示例数据
# NOC,Sport,Year,Athletes
# CHN,Basketball,1936,13
# CHN,Basketball,1948,10
# CHN,Basketball,1984,23
# CHN,Basketball,1988,22
# CHN,Basketball,1992,23
# CHN,Basketball,1996,24
# CHN,Basketball,2000,12
# CHN,Basketball,2004,24
# CHN,Basketball,2008,24
# CHN,Basketball,2012,24
# CHN,Basketball,2016,24
# CHN,Basketball,2020,12
# CHN,Basketball,2024,12


#有一套数据集，里面包含所有国家参加的所有奥运会的运动员数量，数据集格式为NOC,Sport,Year,Athletes，其中NOC表示国家代码，Sport表示体育项目，Year表示年份，Athletes表示参加的运动员数量。
#先要进行线性回归，预测2028年，2032年，2036年中国参加篮球比赛的运动员数量，导出csv文件，列为NOC,Sport,2028,2032,2036

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 读取数据
data = pd.read_csv('./data/n_participants.csv')

#数据预处理
#空值填0
data.fillna(0, inplace=True)


#里面记录了每个Sport项目每年的运动员数，每一行都有从1896年到2024年的运动员数

#我们对每个国家、项目组成的一组数据进行线性回归拟合，预测2028,2032,2036年预期每个项目的运动员数

#创建模型
model = LinearRegression()

#创建一个DataFrame，用于存放预测结果
result = []

#对每一组数据进行拟合

#groupby国家、项目

for name, group in data.groupby(['NOC', 'Sport']):
    #创建X，Y
    X = group['Year'].values.reshape(-1, 1)
    Y = group['Athletes'].values.reshape(-1, 1)
    
    #训练模型
    model.fit(X, Y)
    
    #预测
    predict = model.predict([[2028], [2032], [2036]])
    
    #添加到result，注意需要包括
    result.append([name[0], name[1], predict[0][0], predict[1][0], predict[2][0]])
    
    
#导出结果
result = pd.DataFrame(result, columns=['NOC', 'Sport', '2028', '2032', '2036'])

#和原先的数据合并，注意原先的数据格式为
# NOC,Sport,Year,Athletes
# CHN,Basketball,1936,13
# CHN,Basketball,1948,10
# CHN,Basketball,1984,23
# CHN,Basketball,1988,22
#因此，合并result和data时，每一条result数据要拆分成3条数据，分别对应2028,2032,2036年，然后和data合并

#拆分result
result = pd.melt(result, id_vars=['NOC', 'Sport'], value_vars=['2028', '2032', '2036'], var_name='Year', value_name='Athletes')

#合并
data['Year'] = data['Year'].astype(str)
result['Year'] = result['Year'].astype(str)
data = pd.concat([data, result], axis=0)

#排序数据，根据NOC和Sport排序
data = data.sort_values(['NOC', 'Sport', 'Year'])
#导出

data.to_csv('./data/predict_participants.csv', index=False)

#result.to_csv('./data/predict_participants.csv', index=False)