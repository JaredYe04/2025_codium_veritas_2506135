#summerOly_programs.csv

import pandas as pd
import numpy as np

# 读取数据
data = pd.read_csv('./data/summerOly_programs.csv')

#数据预处理
#空值填0
data.fillna(0, inplace=True)

#首先把一个Sport里面所有的子类都合并到一起
data = data.groupby('Sport').sum().reset_index()
print (data)

#里面记录了每个Sport项目每年的奖牌数，每一行都有从1896年到2024年的奖牌数
#我们对每一行都进行线性回归拟合，预测2028,2032,2036年预期每个项目的奖牌数

#导入线性回归模型
from sklearn.linear_model import LinearRegression

#创建模型
model = LinearRegression()

#创建一个DataFrame，用于存放预测结果
result = []

#对每一行进行拟合
for index, row in data.iterrows():
    #创建X，Y
    X = data.columns[4:].values.reshape(-1, 1)
    Y = row.values[4:].reshape(-1, 1)
    
    #训练模型
    model.fit(X, Y)
    
    #预测
    predict = model.predict([[2028], [2032], [2036]])
    
    #添加到result
    result.append([row['Sport'], predict[0], predict[1], predict[2]])
    

#导出结果
result = pd.DataFrame(result, columns=['Sport', '2028', '2032', '2036'])
result.to_csv('./data/predict_medal_counts.csv', index=False)
    