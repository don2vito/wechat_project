import pandas as pd
import time
from tqdm import tqdm

'''
对 Excel 文件进行多 sheet 合并读取
'''
# 方法一：合并同一工作簿中的所有工作表
time_start = time.time()
result = pd.DataFrame()
dfs = pd.read_excel('./多sheet.xlsx', sheet_name=None).values()
result = pd.concat(dfs)
print(f'合并后的数据如下：\n{result}')
result.to_excel('./合并后结果.xlsx', index=False, freeze_panes=(1,0))
time_end = time.time()
print('共耗时 {}分 {}秒'.format(int(round((time_end - time_start) / 60,0)),round((time_end - time_start) % 60,2)))
print('=======================================================================================')

# 方法二：循环读取同一工作簿中的所有工作表
time_start = time.time()
dfs = pd.read_excel('./多sheet.xlsx', sheet_name=None)
keys = list(dfs.keys())
# print(keys)
result = pd.DataFrame()
num = 1
for i in keys:
    df = dfs[i]
    print(f'第{num}个 sheet 的数据如下：\n{df}')
    result = pd.concat([result,df])
    result.to_excel('./循环合并后结果.xlsx', index=False, freeze_panes=(1,0))
    num += 1
print(f'循环合并后的数据如下：\n{result}')
time_end = time.time()
print('共耗时 {}分 {}秒'.format(int(round((time_end - time_start) / 60,0)),round((time_end - time_start) % 60,2)))
print('=======================================================================================')

'''
大规模 Excel 文件数据读取
'''
'''使用 usecols 参数：指定列'''
# 方法一：使用列表 - 字段顺序数字（从 0 开始）
df1 = pd.read_excel('./多sheet.xlsx', sheet_name='Sheet1',usecols=[0,1,2])
print(f'使用列表 - 字段顺序数字后的数据如下：\n{df1}')
df1.to_excel('./usecols参数示例1.xlsx', index=False, freeze_panes=(1,0))
print('=======================================================================================')

# 方法二：使用列表 - 字段名称文本
df2 = pd.read_excel('./多sheet.xlsx', sheet_name='Sheet2',usecols=['来源','名称'])
print(f'使用列表 - 字段名称文本后的数据如下：\n{df2}')
df2.to_excel('./usecols参数示例2.xlsx', index=False, freeze_panes=(1,0))
print('=======================================================================================')

# 方法三：使用 Excel 字段英文字母（可用冒号 ':' 进行连续范围切片选择，仅支持 pandas 1.1.0 以上版本）
df3 = pd.read_excel('./多sheet.xlsx', sheet_name='Sheet3',usecols='A,C:D')
print(f'使用 Excel 字段英文字母后的数据如下：\n{df3}')
df3.to_excel('./usecols参数示例3.xlsx', index=False, freeze_panes=(1,0))
print('=======================================================================================')

# 方法四：使用自定义函数
def filter_yield(col_name):
    if '名' in col_name:
        return col_name

df4 = pd.read_excel('./多sheet.xlsx', sheet_name='Sheet3',usecols=filter_yield)
print(f'使用自定义函数后的数据如下：\n{df4}')
df4.to_excel('./usecols参数示例4.xlsx', index=False, freeze_panes=(1,0))
print('=======================================================================================')

'''使用 dtype 参数：指定数据类型'''
# 使用字典（dict）的形式
print(f'数据类型修改前：\n{result.info()}')
result = pd.read_excel('./多sheet.xlsx', sheet_name='Sheet1',dtype={'数量':'str'})
print('=======================================================================================')
print(f'数据类型修改后：\n{result.info()}')
print('=======================================================================================')

'''使用 skiprows、skipfooter、nrows 参数：指定部分行'''
df = pd.read_excel('./多sheet.xlsx', sheet_name='Sheet1',skiprows=range(1, 3),nrows=2)
print(f'指定跳过行数后的数据如下：\n{df}')
df.to_excel('./skiprows+nrows参数示例.xlsx', index=False, freeze_panes=(1,0))

print('=======================================================================================')

'''使用 dask 库，不支持 Excel 文件格式'''
import dask.dataframe as dd

# result = pd.DataFrame()
# dfs = pd.read_excel('./【数据集】近一年订购大分类.xlsx', sheet_name=None)
# keys = list(dfs.keys())
# # print(keys)
# result = pd.DataFrame()
# for i in keys:
#     df = dfs[i]
#     result = pd.concat([result,df])
# result.to_csv('./近一年订购大分类.csv', index=False,encoding='utf-8')
# print('Excel 转换 CSV 完成！！')
# print('=======================================================================================')

time_start = time.time()
df = dd.read_csv('./近一年订购大分类.csv')
print(f'合并后的数据如下：\n{df}')
print(df.groupby(df.顾客编号).mean().compute())
time_end = time.time()
print('使用 dask 库读取数据共耗时 {}分 {}秒'.format(int(round((time_end - time_start) / 60,0)),int(round((time_end - time_start) % 60,0))))
print('=======================================================================================')

'''使用 chunksize 参数：指定分块读取的数据量'''
df = pd.read_csv('./近一年订购大分类.csv',chunksize=1000)
result = (pd.concat([chunk.groupby(['顾客编号'], as_index=False).agg({'累计订购数量': 'sum','累计订购金额': 'sum'}) for chunk in tqdm(df)]).groupby(['顾客编号']).agg({'累计订购数量': 'sum','累计订购金额': 'sum'}))
print(f'指定跳过行数后的数据如下：\n{result}')
result.to_csv('./chunksize参数示例.csv', index=False)
print('=======================================================================================')

'''
小技巧
'''
'''在 to_excel() 方法中，使用 freeze_panes 参数：指定需要冻结的行和列'''
# 使用元组 - 从 0 开始，形式为（行数，列数）
# freeze_panes = (1,0) 冻结首行
# freeze_panes = (0,1) 冻结首列
# freeze_panes = (1,1) 冻结首行首列
