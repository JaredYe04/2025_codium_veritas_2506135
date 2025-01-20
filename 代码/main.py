#写一个用于区分鸢尾花的程序，使用KNN算法
#导入数据集
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

#导入数据集
iris_dataset = load_iris()
#划分数据集
X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)
#创建模型
knn = KNeighborsClassifier(n_neighbors=1)
#训练模型
knn.fit(X_train, y_train)
#预测
X_new = np.array([[5, 2.9, 1, 0.2]])
prediction = knn.predict(X_new)
print("预测结果：{}".format(prediction))
print("预测花的种类：{}".format(iris_dataset['target_names'][prediction]))
#评估模型
print("模型评分：{:.2f}".format(knn.score(X_test, y_test)))



#这是一个测试文件