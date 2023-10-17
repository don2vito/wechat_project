import prettytable as pt
import pandas as pd
import re

def re_zh(x):
    str = ''.join(re.findall('[\u4e00-\u9fa5]', x)) 
    return str

def re_en(x):
    str = ''.join(re.findall('[A-Za-z]', x)) 
    return str

def re_num(x):
    str = ''.join(re.findall('\d+', x)) 
    return str


df = pd.read_excel('./正则模拟数据.xlsx',sheet_name='原始数据')
df['中文'] = df['文本列'].apply(re_zh)
df['英文'] = df['文本列'].apply(re_en)
df['数字'] = df['文本列'].apply(re_num)

tb = pt.PrettyTable()
for col in df.columns.values:# 使用 df.columns.values 获取列的名称
    tb.add_column(col, df[col])
print(f'处理后的表格如下：\n{tb}')

df.to_excel('./python_result.xlsx',sheet_name='re_result',index=False,encoding='utf-8')
print('Excel 文件已生成！！')