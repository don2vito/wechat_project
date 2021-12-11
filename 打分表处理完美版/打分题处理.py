import pandas as pd
import re

def get_score(x):
    result_list = re.findall('\d+',x,re.S)
    return result_list[1]

def get_category(x):
    result_list = re.findall('\d+', x, re.S)
    n = len(result_list[1]) * int(-1)
    result = x[0:n]
    return result

df = pd.read_excel('./打分题.xls',sheet_name='问卷调查')
df['顾客编号'] = df['顾客编号'].astype('str')
# df_explode = df[['问题1','问题2','问题3']].apply(lambda x:[y.split('\n') for y in x]).apply(pd.Series.explode)
# df_result = pd.concat([df[['序号','顾客编号']],df_explode],axis=1)
df[['问题1','问题2','问题3']] = df[['问题1','问题2','问题3']].apply(lambda x:[y.split('\n') for y in x])
df_result = df.explode(column=['问题1','问题2','问题3'])
df_result = df_result[df_result['问题1'] != '']
df_result['问题1'] = df_result['问题1'].str.replace(' ','_').str.strip()
df_result['问题2'] = df_result['问题2'].str.replace(' ','_').str.strip()
df_result['问题3'] = df_result['问题3'].str.replace(' ','_').str.strip()
df_result = pd.melt(df_result,id_vars=['序号','顾客编号'],var_name='题目',value_name='分类')
df_result['分数'] = df_result['分类'].apply(get_score)
df_result['分类'] = df_result['分类'].apply(get_category)
df_result['分数'] = df_result['分数'].astype('int')
df_result = df_result.drop_duplicates()
# print(df_result)
df_result = pd.pivot_table(df_result,index=['序号','顾客编号'],columns=['题目','分类'],values=['分数'],aggfunc='sum',fill_value=0)
df_result.to_excel('./处理后打分题.xlsx',sheet_name='处理后')
print(f'表格处理完成！！')