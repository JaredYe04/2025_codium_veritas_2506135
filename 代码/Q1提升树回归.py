#导入训练集，进行LightGBM模型训练
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#导入数据
data=pd.read_csv('./data/train_data.csv')

#is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg,Gold_prob,Silver_prob,Bronze_prob,No_medal_prob,Gold,Silver,Bronze
#其中，最后三列Gold,Silver,Bronze是我们要预测的数值，前面的是特征值
#将数据分为特征值和目标值
X=data.iloc[:,0:-3]
Y=data.iloc[:,-3:]

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


#导入lightgbm模型
import lightgbm as lgb

#划分训练集和测试集
from sklearn.model_selection import train_test_split

#由于Y有三列，因此需要分别训练三个模型
#第一个模型预测Gold
models=['Gold','Silver','Bronze']

performances=[]

for modelName in models:
    Y=data[modelName]
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=0)
    #创建模型
    model=lgb.LGBMRegressor()
    #训练模型
    model.fit(X_train,Y_train)
    
    #预测
    Y_predict=model.predict(X_test)
    #评估
    from sklearn.metrics import mean_squared_error
    mse=mean_squared_error(Y_test,Y_predict)
    print(modelName+'的均方误差为：',mse)
    
    #由于获奖牌是少数，因此需要评价召回率
    #将预测值四舍五入
    Y_predict=np.round(Y_predict)
    
    # import joblib
    # joblib.dump(model,'./models/'+modelName+'.pkl')
    
    #均方根误差
    from sklearn.metrics import mean_squared_error
    rmse=mean_squared_error(Y_test,Y_predict)**0.5
    print(modelName+'的均方根误差为：',rmse)
    
    #平均绝对误差
    from sklearn.metrics import mean_absolute_error
    mae=mean_absolute_error(Y_test,Y_predict)
    print(modelName+'的平均绝对误差为：',mae)
    
    #R2
    from sklearn.metrics import r2_score
    r2=r2_score(Y_test,Y_predict)
    print(modelName+'的R2为：',r2)
    
    performances.append([modelName,mse,rmse,mae,r2])
    
    #ROC曲线
    from sklearn.metrics import roc_curve
    fpr,tpr,thresholds=roc_curve(Y_test,Y_predict)
    plt.plot(fpr,tpr)
    plt.show()
    
    
    
    
    
    