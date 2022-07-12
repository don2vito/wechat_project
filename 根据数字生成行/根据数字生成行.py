import pandas as pd

df = pd.read_excel('./根据数字生成行.xlsx',sheet_name='test')

df['index'] = df.apply(lambda x: list(range(x['num'])), axis=1)
df_result = df.explode('index')
print(df_result)