#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from alive_progress import alive_bar
import xlwings as xw
import warnings

target_file = './结果表.xlsx'

df = pd.read_excel('./test.xlsx',sheet_name='Sheet1')
df


# In[2]:


# 生成笛卡尔积

df_a = pd.DataFrame(df['地域'])
df_b = pd.DataFrame(df['省份'])
df_c = pd.DataFrame(df['产品年'])

df_a['临时列'] = 1
df_b['临时列'] = 1
df_c['临时列'] = 1
  
df_dikaer = pd.merge(df_a,df_b,on='临时列')
df_dikaer = pd.merge(df_dikaer,df_c,on='临时列')                    

df_dikaer = df_dikaer.drop('临时列',axis=1)
df_dikaer.drop_duplicates(inplace=True)
df_dikaer.head()


# In[3]:


# 关联（左连接）

df = pd.merge(df_dikaer,df,on=['地域','省份','产品年'],how='left').fillna(0)
df.head()


# In[4]:


df_pivot = pd.pivot_table(df,index=['地域','产品年'],columns=['省份'],values=['数量','金额','市值'],aggfunc='sum', margins=True,fill_value=0)
df_pivot


# In[5]:


df_subtotal = df_pivot.stack('省份').fillna(0).reset_index()
df_subtotal = df_subtotal[df_subtotal['地域']!='All']
df_subtotal['省份'] = df_subtotal['省份'].str.replace('All','小计')
df_subtotal


# In[6]:


# 注意！此时“列”的纵向总计由于小计的存在，数值是实际值的 2 倍，需要后续处理（横向是无问题的）

df_pivot = pd.pivot_table(df_subtotal,index=['地域','省份'],columns=['产品年'],values=['数量','金额','市值'],aggfunc='sum',fill_value=0, margins=True,margins_name='总计')
df_pivot = df_pivot.drop(('总计','' ), axis=0)
df_pivot.loc[('总计','' ),:] = df_pivot.sum(axis=0) / 2
df_pivot


# In[7]:


# 自定义列字段的顺序（适用于多层索引的调换顺序、排序）

# 交换层级
df_pivot = df_pivot.reorder_levels([1,0],axis=1)

# # 自定义顺序
# 构建元组

cols_new = []

a = [2020,2021,2022,'总计']
b = ['数量','金额','市值']

for i in a:
    for m in b:
        list_temp = []
        list_temp.append(i)
        list_temp.append(m)
        cols_new.append(tuple(list_temp))
        
df_pivot = df_pivot[cols_new]

df_pivot = df_pivot.sort_index(axis=1)
df_pivot = df_pivot.astype('float').reset_index()
df_pivot


# In[8]:


# 自定义行字段的顺序（手动指定），自动指定用 sort_index()

type1 = pd.CategoricalDtype(categories=['A','B','C','总计'],ordered=True)
type2 = pd.CategoricalDtype(categories=['甲','乙','丙','丁','戊','己','小计',''],ordered=True)
df_pivot[('地域',   '')] = df_pivot[('地域',   '')].astype(type1)  #将指定列转成自定义的type
df_pivot[('省份',   '')] = df_pivot[('省份',   '')].astype(type2)
df_pivot.sort_values(by=[('地域',   ''),('省份',   '')],inplace=True)
df_pivot


# In[9]:


# 姜两层列名恢复成单层

df_pivot.columns =[str(s1) +' '+ str(s2) for (s1,s2) in df_pivot.columns.tolist()]
df_pivot = df_pivot.reset_index(drop=True)
df_pivot


# In[10]:


# 持久化输出

with pd.ExcelWriter(target_file) as writer:
    df_pivot.to_excel(writer,sheet_name='result', index=False)

app = xw.App(visible=False,add_book=False)
workbook = app.books.open('./结果表.xlsx')

with alive_bar(len(workbook.sheets)) as bar:    
    for i in workbook.sheets:
        bar()
        # pbar.set_description(f'Processing {i}')
    # 批量设置格式（行高、列宽、字体、大小、线框）
        value = i.range('A1').expand('table')# 选择要调整的区域
        value.rows.autofit() # 调整列宽字符宽度
        value.columns.autofit()  # 调整行高字符宽度
        value.api.Font.Name = '微软雅黑' # 设置字体
        value.api.Font.Size = 9 # 设置字号大小（磅数）
        value.api.VerticalAlignment = xw.constants.VAlign.xlVAlignCenter # 设置垂直居中
        value.api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter # 设置水平居中
        for cell in value:
            for b in range(7,12):
                cell.api.Borders(b).LineStyle = 1 # 设置单元格边框线型
                cell.api.Borders(b).Weight = 2 # 设置单元格边框粗细
        value = i.range('A1').expand('right')  # 选择要调整的区域
        value.api.Font.Size = 10
        value.api.Font.Bold = True  # 设置为粗体
        # print(f'《{i.name}》 页面处理完成……')
workbook.save()
workbook.close()
app.quit()

print(f'\n表格输出完成！！')

