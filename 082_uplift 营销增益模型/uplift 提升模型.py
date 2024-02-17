import pandas as pd
import numpy as np
import toad 
from sklearn.model_selection import train_test_split
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据集
  # - recency: 上次购买距离现在的月数
  # - history: 历史购买的金额
  # - used_discount / used_bogo: 表示用户是否使用了折扣或者买一送一
  # - zip_code: 邮编的类型有农村 / 郊区 / 城市
  # - is_referral: 表示用户是否通过 referral（转介、推荐） 获得
  # - channel: 客户使用的渠道，电话 / 网站 / 多通道
  # - offer: 发给用户的优惠，打折 / 买一送一 //无优惠
  # - conversion：是否响应
data = pd.read_csv("uplift-data.csv")
print(data.head())

# 查看数据信息
print(toad.detector.detect(data))

# 替换字符串
zip_code_dic={
    'Surburban':1,
    'Urban':2,
    'Rural':3
}
channel_dic={
    'Web':1,
    'Phone':2,
    'Multichannel':3
}
offer_dic={
    'Buy One Get One':1,
    'Discount':2,
    'No Offer':0
}

data = data.replace({'zip_code': zip_code_dic,
                     'channel':channel_dic,
                     'offer':offer_dic})

# 计算活动提升情况
def calc_uplift(df):
    # 计算各活动方式的转化率
    base_conv = df[df.offer == 0]['conversion'].mean()
    disc_conv = df[df.offer == 2]['conversion'].mean()
    bogo_conv = df[df.offer == 1]['conversion'].mean()
    
    # 计算两活动转化率的提升效果
    disc_conv_uplift = disc_conv - base_conv
    bogo_conv_uplift = bogo_conv - base_conv
    
    print('Discount Conversion Uplift: {0}%'.format(np.round(disc_conv_uplift*100,2)))
    
    if len(df[df.offer == 1]['conversion']) > 0:
          
        print('-'*60)
        print('BOGO Conversion Uplift: {0}%'.format(np.round(bogo_conv_uplift*100,2)))

# 根据 uplift score 计算方式进行分类
# 设置对照-实验组
data['campaign_group'] = 1
data.loc[data.offer == 0, 'campaign_group'] = 0

# 分类
data['target_class'] = 0 # CN
data.loc[(data.campaign_group == 0) & (data.conversion == 1),'target_class'] = 1 # CR
data.loc[(data.campaign_group == 1) & (data.conversion == 0),'target_class'] = 2 # TN
data.loc[(data.campaign_group == 1) & (data.conversion == 1),'target_class'] = 3 # TR

# 模型数据
df_model = data.drop(['offer','campaign_group','conversion'],axis=1) 
print(df_model.head())

# 拆分样本
X = df_model.drop(['target_class'],axis=1)
y = df_model.target_class
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=56)

# XGB 分类模型训练
param_dist = {'objective':'multi:softmax', 'eval_metric':'logloss', 'use_label_encoder':False}
model_xgb = xgb.XGBClassifier(**param_dist)
model_xgb.fit(X_train, y_train)

# 计算 uplift_score
y_prob = model_xgb.predict_proba(X)
uplift_score=[]
for i in y_prob:
    us=i[0]+i[3]-i[1]-i[2]
    uplift_score.append(us)
data['uplift_score'] = uplift_score
print(data.head())

# 模型评估
# 记录活动的base
print(calc_uplift(data))

# 高 uplift 分数：客户的 uplift 分数 > 3/4 分位数
data_lift = data.copy()
uplift_q_75 = data_lift.uplift_score.quantile(0.75)
data_lift = data_lift[data_lift.uplift_score > uplift_q_75].reset_index(drop=True)
# 计算 top 1/4 的用户的提升情况
print(calc_uplift(data_lift))

# 低 uplift 分数：客户的 uplift 分数 < 1/2 分位数
data_lift = data.copy()
uplift_q_50 = data_lift.uplift_score.quantile(0.5)
data_lift = data_lift[data_lift.uplift_score < uplift_q_50].reset_index(drop=True)
# 计算 bottom 1/2 的用户的提升情况
calc_uplift(data_lift)

# 评分直方图
def plot_score_hist(df, y_col, score_col, cutoff=None):
    """
    df:数据集（含y_col,score列）
    y_col:目标变量的字段名
    score_col:得分的字段名
    cutoff :划分拒绝/通过的点
    
    return :不同类型用户的得分分布图
    """  
    # 预处理
    x1 = df[df[y_col] == 0][score_col]
    x2 = df[df[y_col] == 1][score_col]
    x3 = df[df[y_col] == 2][score_col]
    x4 = df[df[y_col] == 3][score_col]
    # 绘图
    plt.figure(dpi=300)
    plt.title('Uplift Score Hist')
    sns.kdeplot(x1,fill=True,label='CN')
    sns.kdeplot(x2,fill=True,label='CR')
    sns.kdeplot(x3,fill=True,label='TN')
    sns.kdeplot(x4,fill=True,label='TR')
    if cutoff != None:
        plt.axvline(x=cutoff)
    plt.legend()
    return plt

plot_score_hist(data, 'target_class', 'uplift_score')
plt.show()
