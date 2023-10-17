import pandas as pd

# 读取 Excel 数据
df_origin = pd.read_excel('../toy_data .xlsx')

# 分组合并文本
df_group_concat = df_origin.groupby('name').apply(lambda x:'-'.join(x['text'])).reset_index().rename({0:'text'},axis=1)

# 拆分文本
df_group_concat[['text1','text2','text3','text4']] = df_group_concat['text'].str.split('-',expand=True)
df_split = df_group_concat.drop('text',axis = 1)

# 导出 Excel文件
df_split.to_excel('./example_python.xlsx',sheet_name='result',index=False) 