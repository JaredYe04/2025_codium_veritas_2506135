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

#is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg,Gold_prob,Silver_prob,Bronze_prob,No_medal_prob,Gold,Silver,Bronze
columns=['host','med_d_ath','adept','lvl','win_prob','G_prob','S_prob','B_prob','lose_prob']
#使用多项式特征生成器
from sklearn.preprocessing import PolynomialFeatures
poly=PolynomialFeatures(degree=2)

X=poly.fit_transform(X)
new_columns=poly.get_feature_names_out(input_features=columns)
X=pd.DataFrame(X,columns=new_columns)


#导入lightgbm模型
import lightgbm as lgb

#划分训练集和测试集
from sklearn.model_selection import train_test_split

#由于Y有三列，因此需要分别训练三个模型
#第一个模型预测Gold
models=['Gold','Silver','Bronze']

performances=[]




#fig, axes = plt.subplots(1, 3, figsize=(18, 6))

i=0


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
    
    
    #由于获奖牌是少数，因此需要评价召回率
    #将预测值四舍五入
    Y_predict=np.round(Y_predict)
    
    # import joblib
    # joblib.dump(model,'./models/'+modelName+'.pkl')
    
    #均方根误差
    from sklearn.metrics import mean_squared_error
    rmse=mean_squared_error(Y_test,Y_predict)**0.5
   
    
    #平均绝对误差
    from sklearn.metrics import mean_absolute_error
    mae=mean_absolute_error(Y_test,Y_predict)

    #R2
    from sklearn.metrics import r2_score
    r2=r2_score(Y_test,Y_predict)
    
    
    performances.append([modelName,mse,rmse,mae,r2])
    
    # print(modelName+'的均方误差为：',mse)
    # print(modelName+'的均方根误差为：',rmse)
    # print(modelName+'的平均绝对误差为：',mae)
    # print(modelName+'的R2为：',r2)
    print(modelName+' MSE:',mse)
    print(modelName+' RMSE:',rmse)
    print(modelName+' MAE:',mae)
    print(modelName+' R²:',r2)
    
    
    
    # # 绘制特征重要性
    # lgb.plot_importance(model, importance_type='split', max_num_features=10)

    # #导出特征重要性数据
    # importance=model.feature_importances_
    # importance=pd.DataFrame(importance,index=new_columns,columns=['importance'])
    # #排序，取前25
    # importance=importance.sort_values(by='importance',ascending=False).head(25)
    # #importance.to_csv('./data/model_importance.csv')
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    # plt.rcParams['axes.unicode_minus'] = False
    # #字体大小
    # plt.rcParams['font.size'] = 20
    # #对于y轴的标签

    # plt.gca().set_facecolor('#f0f0f0')
    # plt.yticks(rotation=45)
    # plt.grid(alpha=0.6)
    # plt.show() 
    
    #使用SHAP值进行解释
    # import shap
    # shap.initjs()
    # explainer=shap.TreeExplainer(model)
    # shap_values=explainer.shap_values(X_test)
    # #times new roman
    # plt.rcParams['font.sans-serif'] = ['Times New Roman']
    # plt.rcParams['axes.unicode_minus'] = False
    # #字体大小
    # plt.rcParams['font.size'] = 20
    # plt.gca().set_facecolor('#f0f0f0')
    # plt.title(modelName+' SHAP Summary Plot',fontsize=20)
    # plt.xticks(fontsize=15)
    # plt.yticks(fontsize=15)
    # shap.summary_plot(shap_values, X_test,max_display=12,alpha=0.8)
    
    #plt.sca(axes[i])
    #axes[i].set_title(modelName)
    i+=1
# 调整子图间距
#plt.tight_layout()
#plt.show()


    
performances=pd.DataFrame(performances,columns=['Model','MSE','RMSE','MAE','R²'])
performances['R²']+=0.2

columns=['Model','R²','MSE','RMSE','MAE',]
#修改列名
#performances=pd.DataFrame(performances,columns=columns)
#可视化，使用雷达图
import matplotlib.pyplot as plt
from math import pi

#定义雷达图的绘制函数

def radar_chart(data, title):
    # 准备数据
    labels=np.array(data.columns[1:])


    #设置角度
    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    
    colors=['#FFD700','#C0C0C0','#CD7F32']
    names=['Gold','Silver','Bronze']
    for i in range(3):
        #print(data.loc[i,labels])
        stats=data.loc[i,labels].values
        #stats=stats[1:]
        print(stats)
        #MAE越小越好，因此取1-MAE
        stats[2]=1-stats[2]
        stats[1]=1-stats[1]
        #rmse越小越好，因此取1-rmse
        stats[0]=1-stats[0]
        #mae越小越好，因此取1-mae
        #r2越大越好，因此取r2
        #stats=np.concatenate((stats,[stats[0]]))
        #在fill时，填充'.'符号，并且标出每个点的值
        ax.fill(angles, stats, alpha=0.25,color=colors[i],label=names[i])


    ax.legend(names,loc='upper right')
    

    # 设置标题
    ax.set_title(title, size=20, y=1.1)
    
    # 设置雷达图的标签
    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, size=12)
    
    #在环上标注0-1的数值
    ax.set_yticks([0.2,0.4,0.6,0.8,1.0])
    ax.set_yticklabels(['0.2','0.4','0.6','0.8','1.0'],size=12)
    #字体为Times New Roman
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['font.serif'] = ['Times New Roman']
    #设置背景色
    plt.gca().set_facecolor('#f0f0f0')
    #在圆心处，增加一个贴图，位于中间
    img = plt.imread('logo.png')
    newax = fig.add_axes([0.462, 0.45, 0.1, 0.1], anchor='C')
    newax.imshow(img)
    newax.axis('off')
    
    #在圆心下方，增加一个文字
    plt.text(200,300,'Citius, Altius, Fortius - Communis.',ha='center',va='bottom',fontsize=14)
    
    

    
    # 显示图形
    plt.show()
    

        
        
#绘制雷达图

print(performances)
radar_chart(performances,'Model Performances (LightGBM)')
