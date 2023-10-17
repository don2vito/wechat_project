import pandas as pd

df = pd.read_excel('./根据数字生成行.xlsx',sheet_name='test')

# 方法一
df1 = df.copy()
df1['index'] = df1.apply(lambda x: list(range(x['num'])), axis=1)
df_result = df1.explode('index')
print(f'方法一的结果：\n{df_result}')

# 方法二
df2 = df.copy()
df_result = df2.agg(lambda x:x.repeat(df2['num']))
print(f'方法二的结果：\n{df_result}')