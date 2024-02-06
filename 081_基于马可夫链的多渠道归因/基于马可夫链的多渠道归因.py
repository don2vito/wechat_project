# 方法一：MarkovAttribution 方法

# pip install MarkovAttribution

import pandas as pd
from markovattribution import MarkovAttribution

# 读取数据
# 1. 最后一列为是否转化，列名固定为 conv_flag，枚举值为（'null' or 空【即NaN】、'conv'）
# 2. 首列至倒数第二列为渠道流转路径，缺失为空
df1 = pd.read_excel('./数据集-基于马可夫链的多渠道归因.xlsx',sheet_name='MarkovAttribution方法')
print(df1)

#      T_1   T_2   conv_flag
# 0   百度  NaN  conv
# 1   百度  NaN   NaN
# 2  小红书  NaN  conv
# 3   抖音  NaN  conv
# 4   百度   抖音  conv
# 5   百度   抖音   NaN
# 6   抖音  小红书  conv

# 模型拟合
attribution = MarkovAttribution()
ma = attribution.fit(df1)

# 输出结果
for key, value in ma['Markov Values'].items():
    print (key.ljust(5), round(value,2))
    
# 百度              1.67
# 抖音              1.83
# 小红书             1.5


# 方法二：ChannelAttribution 方法

# pip install Cython
# pip install ChannelAttribution

from ChannelAttribution import *

# 读取数据
# path：转化路径，以 > 连接
# total_conversions：累计转化次数
# total_conversion_value：累计转化收益
# total_null：累计未转化次数
df2 = pd.read_excel('./数据集-基于马可夫链的多渠道归因.xlsx',sheet_name='ChannelAttribution方法')
print(df2) 

#      path  total_conversions  total_conversion_value  total_null
# 0      百度                  1                      10           1
# 1     小红书                  1                      10           0
# 2      抖音                  1                      10           0
# 3   百度>抖音                  1                      10           1
# 4  抖音>小红书                  1                      10           0

# markov 算法计算各渠道转化次数和转化收益
result = auto_markov_model(df2, 'path', 'total_conversions', 'total_null', var_value='total_conversion_value')
print(result)

# Suggested order: 1
# Number of simulations: 100000 - Convergence reached: 1.22% < 5.00%
# Percentage of simulated paths that successfully end before maximum number of steps (3) is reached: 99.99%

#   channel_name  total_conversions  total_conversion_value
# 0           百度           1.653302               16.533019
# 1          小红书           1.343396               13.433962
# 2           抖音           2.003302               20.033019