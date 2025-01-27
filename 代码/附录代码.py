
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv('./data/train_data.csv')
X=data.iloc[:,0:-3]
Y=data.iloc[:,-3:]

X.fillna(0,inplace=True)
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
X=scaler.fit_transform(X)
columns=['host','med_d_ath','adept','lvl','win_prob','G_prob','S_prob','B_prob','lose_prob']
from sklearn.preprocessing import PolynomialFeatures
poly=PolynomialFeatures(degree=2)

X=poly.fit_transform(X)
new_columns=poly.get_feature_names_out(input_features=columns)
X=pd.DataFrame(X,columns=new_columns)
import lightgbm as lgb
from sklearn.model_selection import train_test_split
models=['Gold','Silver','Bronze']
performances=[]
i=0
for modelName in models:
    Y=data[modelName]
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=0)
    model=lgb.LGBMRegressor()
    model.fit(X_train,Y_train)
    Y_predict=model.predict(X_test)
    from sklearn.metrics import mean_squared_error
    mse=mean_squared_error(Y_test,Y_predict)
    Y_predict=np.round(Y_predict)
    from sklearn.metrics import mean_squared_error
    rmse=mean_squared_error(Y_test,Y_predict)**0.5
    from sklearn.metrics import mean_absolute_error
    mae=mean_absolute_error(Y_test,Y_predict)
    from sklearn.metrics import r2_score
    r2=r2_score(Y_test,Y_predict)
    performances.append([modelName,mse,rmse,mae,r2])
    print(modelName+' MSE:',mse)
    print(modelName+' RMSE:',rmse)
    print(modelName+' MAE:',mae)
    print(modelName+' R²:',r2)
    
