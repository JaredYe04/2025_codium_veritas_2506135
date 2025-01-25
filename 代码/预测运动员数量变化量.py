#athlete_number_variation.csv

#在原来数据集的基础上，保留原来的数据，并进行线性回归，预测2028,2032,2036年运动员人数的变化趋势，导出csv文件，列为NOC,Sport,Year,Change

#原始数据示例
# NOC,Sport,Year,New,Leave
# CHN,Basketball,1992,16,15
# CHN,Basketball,2012,13,13
# CHN,Basketball,1920,0,0
# CHN,Basketball,1900,0,0
# CHN,Basketball,1932,0,0
# CHN,Basketball,1952,0,10
# CHN,Basketball,2000,4,16
# CHN,Basketball,1996,13,12
# CHN,Basketball,1912,0,0
# CHN,Basketball,1924,0,0
# CHN,Basketball,1948,10,0
# CHN,Basketball,2008,13,13

#首先把New线性回归的变量，预测2028,2032,2036年的变化趋势，导出csv文件，列为NOC,Sport,Year,New,Leave,Leave为0
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
# 读取数据
data = pd.read_csv('./data/athlete_number_variation.csv')


#创建模型
model = LinearRegression()

#创建一个DataFrame，用于存放预测结果
result = []

#对每一组数据进行拟合

#groupby国家、项目

for name, group in data.groupby(['NOC', 'Sport']):
    #创建X，Y
    X = group['Year'].values.reshape(-1, 1)
    Y = group['New'].values.reshape(-1, 1)
    
    #训练模型
    model.fit(X, Y)
    
    #预测
    predict = model.predict([[2028], [2032], [2036]])
    
    #添加到result
    result.append([name[0],name[1],2028,predict[0][0],0])
    result.append([name[0],name[1],2032,predict[1][0],0])
    result.append([name[0],name[1],2036,predict[2][0],0])
    
    
#与原来的data合并
result = pd.DataFrame(result, columns=['NOC', 'Sport', 'Year', 'New', 'Leave'])
data = pd.concat([data,result])

#排序数据

data = data.sort_values(['NOC', 'Sport', 'Year'])
data.to_csv('./data/predict_athlete_number_variation.csv', index=False)
#导出结果