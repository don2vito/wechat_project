#!/usr/bin/env python
# coding: utf-8

# ![af0518c807adfef994ecf938b7e7abd.png](attachment:04ade9cd-172e-4bdd-8f74-9f7fbe849935.png)
# 
# ![ce58bed276ef438fdcb51be95450913.png](attachment:42629c43-fdf0-4b2e-a450-315d1dc0c8fe.png)

# In[1]:


import pandas as pd


# In[2]:


# 载入原始表

df = pd.read_excel('./横板转竖版.xlsx',sheet_name='Sheet1')
df.head()


# In[3]:


# 逆透视

df = df.melt(id_vars='SKU#')
df


# In[4]:


# 剔除含有空值的行

df = df.dropna(axis=0, how='any')
df


# In[5]:


# 一行转多行

df['value_processed'] = df['value'].str.split('；')
df = df.explode('value_processed')
df['story_package'] = df['variable'] + '-' + df['value_processed']
df_result = df[['SKU#','story_package']]
df_result

