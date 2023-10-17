import pandas as pd
import numpy as np

df = pd.read_excel('./脱敏数据.xls',sheet_name='sheet1')
pivot_df = pd.pivot_table(df,values=['On-Air数量','On-Air金额'],index=['事业部名称'],aggfunc=[np.sum],fill_value=0,margins=True,margins_name='合计')
pivot_df.to_excel('./数据透视表_pandas.xls',sheet_name='pandas')
print(f'输出完成！')
