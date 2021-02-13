import pandas as pd
import os
import math

'''按指定分类拆分'''
print('按指定分类拆分：')
data = pd.read_excel('./示例文件.xlsx')
data_list = list(data['世代'].drop_duplicates()) # 去重处理
length = len(data_list) # 计算共有多少数量

path = './split_excel_by_category'
if not os.path.exists(path): # 当前文件夹下是否有此文件夹
    os.mkdir(path) # 创建此文件夹

count = 0
for item in data_list:
    data_select = data[data['世代']==item] # 选出item对应的行
    data_select.to_excel('./split_excel_by_category/{}.xlsx'.format(item),index=False) # 按照对应的值生成 EXCEL 文件
    count += 1
    print('\rEXCEL表中共有 {} 个名称，正在拆分第 {} 个数据，拆分进度：{:.2%}'.format(length, count, count / length),end="")
print('\n{}个名称已经全部拆分完毕，请前往 split_excel_by_category 文件夹下查看拆分后的各文件数据'.format(length))
print('==========================================================================================================')

'''按指定行数拆分'''
print('按指定行数拆分：')
path = './split_excel_by_rows'
if not os.path.exists(path): # 当前文件夹下是否有此文件夹
    os.mkdir(path) # 创建此文件夹

df = pd.read_excel('./示例文件.xlsx')
rows,cols = df.shape # 获取行数列数,默认第一行表头不算行数

split_num = 10 # 指定分割行数
value = math.floor(rows/split_num) # 标准分割次数
rows_format = value*split_num # 标准分割所占用总行数
new_list = [[i,i+split_num] for i in range(0,rows_format,split_num)]

# 标准行数文件
count = 0
for i_j in new_list:
    i,j = i_j
    excel_small = df[i:j]
    # index 为 False,否则就把行索引写入了
    excel_small.to_excel('./split_excel_by_rows/{0}_{1}.xlsx'.format(i,j),index=False)
    count += 1
    print('\rEXCEL表中共有 {} 个名称，正在拆分第 {} - {}的数据，拆分进度：{:.2%}'.format(value, i,j, count / value), end="")

# 最后分割出的文件
df[rows_format:].to_excel('./split_excel_by_rows/last.xlsx')
print('\n{}个名称已经全部拆分完毕，请前往 split_excel_by_category 文件夹下查看拆分后的各文件数据'.format(value))
print('==========================================================================================================')