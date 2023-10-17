import pandas as pd

def float2pct(x):
    pct = '%.2f%%' % (x * 100)
    # pct = str(round(x * 100,2)) + '%'
    return pct

df = pd.read_excel('./分组占比模拟数据.xlsx',sheet_name='原始数据')
df_group = df.groupby(['事业部'])['指标'].sum().reset_index()
df_merge = pd.merge(df,df_group,on='事业部',how='inner')
df_merge.columns = ['事业部','部门','指标','组内指标合计数']
df_merge['组内占比'] = df_merge['指标'] / df_merge['组内指标合计数']
df_merge = df_merge.sort_values(by=['事业部','组内占比'],ascending=[True,False])
df_merge['组内排名（降序）'] = df_merge['指标'].groupby(df_merge['事业部']).rank(method='min',ascending=False).astype(int)
df_merge['组内占比（百分比）'] = df_merge['组内占比'].apply(float2pct)
df_merge = df_merge.drop(columns = ['组内指标合计数'])
print(df_merge.info())
df_merge_io = df_merge[['事业部','部门','指标','组内占比（百分比）','组内排名（降序）']]
# 在已有 Excel 文件中生成新的 sheet
writer=pd.ExcelWriter('./python_result.xlsx',mode='a',engine='openpyxl')
df_merge_io.to_excel(writer,sheet_name='group_pct_result', index=False)
writer.save()
writer.close()
print('Excel 文件已生成！！')

# 取组内降序排名前五
df_top5 = df_merge[df_merge['组内排名（降序）'] <= 5]
df_top5 = df_top5[['事业部','部门','指标','组内占比（百分比）','组内排名（降序）']]
print(df_top5)

# 取组内占比超过20%
df_over_20pct = df_merge[df_merge['组内占比'] > 0.2]
df_over_20pct = df_over_20pct[['事业部','部门','指标','组内占比（百分比）','组内排名（降序）']]
print(df_over_20pct)