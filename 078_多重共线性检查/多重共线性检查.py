import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


# 读取数据（自变量）
df = pd.read_csv("./boston_housing_data.csv",sep=",")
df = df.iloc[:,0:-1]

# 添加一个截距列
X = sm.add_constant(df)

# 计算 VIF 值
# VIF 值越高，表示共线性问题越严重
# 通常，VIF 值大于 5 或 10 被认为是存在多重共线性的迹象
vif = pd.DataFrame()
vif["Features"] = X.columns
vif["VIF Factor"] = [variance_inflation_factor(X.values,i) for i in range(X.shape[1])]
vif["VIF Factor"] = vif["VIF Factor"].round(decimals=0)
vif["VIF Factor"] = vif["VIF Factor"].astype("int")
vif["T/F"] = vif["VIF Factor"].apply(lambda x:True if x >= 10 else False)
vif = vif.sort_values(by="VIF Factor",ascending=False)

print(vif[vif["T/F"] == True])

#   Features  VIF Factor   T/F
# 9      RAD         167  True
# 0    const         114  True
# 6       RM          78  True
# 5      NOX          40  True
# 8      DIS          34  True


# 加载波士顿房价数据集
from sklearn.datasets import load_boston
boston = load_boston()

# 创建一个DataFrame来存储数据集的特征
df = pd.DataFrame(boston.data, columns=boston.feature_names)

# 添加目标变量
# df['PRICE'] = boston.target

# 计算特征之间的相关系数矩阵
corr_matrix = df.corr()

# 计算VIF
vif = pd.DataFrame()
vif["Features"] = corr_matrix.index
vif["VIF Factor"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]

print(vif)