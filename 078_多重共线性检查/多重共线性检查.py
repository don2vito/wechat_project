import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


# 读取数据（自变量）
df = pd.read_csv("./boston_housing_data.csv",sep=",")
df = df.iloc[:,0:-1]


# 1- CRIM     犯罪率；per capita crime rate by town
# 2- ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
# 3- INDUS    非零售商业用地占比；proportion of non-retail business acres per town
# 4- CHAS     是否临Charles河；Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
# 5- NOX      氮氧化物浓度；nitric oxides concentration (parts per 10 million)
# 6- RM       房屋房间数；average number of rooms per dwelling
# 7- AGE      房屋年龄；proportion of owner-occupied units built prior to 1940
# 8- DIS      和就业中心的距离；weighted distances to five Boston employment centres
# 9- RAD      是否容易上高速路；index of accessibility to radial highways
# 10- TAX      税率；full-value property-tax rate per $10,000
# 11- PTRATIO  学生人数比老师人数；pupil-teacher ratio by town
# 12- B        城镇黑人比例计算的统计值；1000(Bk - 0.63)^2 where Bk is the proportion of black people by town
# 13- LSTAT    低收入人群比例；% lower status of the population


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
# from sklearn.datasets import load_boston
# boston = load_boston()

# 创建一个DataFrame来存储数据集的特征
# df2 = pd.DataFrame(boston.data, columns=boston.feature_names)

# 添加目标变量
# df['PRICE'] = boston.target

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep=r"\s+", skiprows=22, header=None)
df2 = pd.DataFrame(np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]]))
# target = raw_df.values[1::2, 2]

# 添加一个截距列
Y = sm.add_constant(df2)

# 计算特征之间的相关系数矩阵
# corr_matrix = X.corr()

# 计算VIF
vif2 = pd.DataFrame()
vif2["Features"] = Y.columns
vif2["VIF Factor"] = [variance_inflation_factor(Y.values, i) for i in range(Y.shape[1])]
vif2["VIF Factor"] = vif2["VIF Factor"].round(decimals=0)
vif2["VIF Factor"] = vif2["VIF Factor"].astype("int")
vif2["T/F"] = vif2["VIF Factor"].apply(lambda x:True if x >= 10 else False)
vif2 = vif2.sort_values(by="VIF Factor",ascending=False)

print(vif2[vif2["T/F"] == True])

#   Features  VIF Factor   T/F
# 0    const         585  True