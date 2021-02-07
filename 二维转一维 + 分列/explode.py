import pandas as pd

df = pd.read_excel('./explode.xlsx', sheet_name = 'Sheet1')
df['字段'] = df['字段'].str.split(';')
df = df.explode('字段')
df = df['字段'].str.split(':',expand=True)
df.columns = ['设备','设备号']
print(df)