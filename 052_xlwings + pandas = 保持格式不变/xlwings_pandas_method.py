import xlwings as xw
import pandas as pd
import numpy as np

app = xw.App(visible=False,add_book=False)
workbook = app.books.open('./脱敏数据.xls')
worksheet = workbook.sheets['sheet1']
df = worksheet.range('A1').expand('table').options(pd.DataFrame).value
pivot_df = pd.pivot_table(df,values=['On-Air数量','On-Air金额'],index=['事业部名称'],aggfunc=[np.sum],fill_value=0,margins=True,margins_name='合计')
worksheet_temp = workbook.sheets.add(name='xlwings_pandas')
worksheet_temp.range('A1').value = pivot_df
workbook.save('./数据透视表_xlwings_pandas.xls')
workbook.close()
app.quit()
print(f'输出完成！')