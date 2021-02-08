import pandas as pd

# 方法一：pandas
df = pd.read_excel('./explode.xlsx', sheet_name = 'Sheet1')
df['字段'] = df['字段'].str.split(';')
df = df.explode('字段')
df = df['字段'].str.split(':',expand=True)
df.columns = ['设备','设备号']
print(f'使用 pandas 方法处理结果如下：\n{df}')

# 方法二：正则表达式
import re
df = pd.read_excel('./explode.xlsx', sheet_name = 'Sheet1')
df['处理列'] = df['字段'].map(lambda x:re.findall(r'([A-z]+):([A-z0-9]+)',x))
print('处理后的列如下：\n{}'.format(df['处理列']))
df = df.explode('处理列')
'''写法一'''
df = df.join(pd.DataFrame(df['处理列'].values.tolist(), columns=['设备','设备号']))
'''写法二'''
# df['设备'] = df['处理列'].str[0]
# df['设备号'] = df['处理列'].str[1]
'''写法三'''
# df['设备'] = df['处理列'].map(lambda x:x[0])
# df['设备号'] = df['处理列'].map(lambda x:x[1])
df = df.drop(columns=['处理列'])
print(f'使用正则表达式方法处理结果如下：\n{df}')