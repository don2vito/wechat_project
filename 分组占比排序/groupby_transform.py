import prettytable as pt
import pandas as pd

# 用均值填充缺失值
# df['value'] = df.groupby(['A']).transform(lambda x:x.fillna(x.mean()))

# 直接增加分组求和值的列
# df['value_sum'] = df.groupby('A')['B'].transform('sum')

# 修改百分比格式（文本）
# df['pct'] = df['pct'].apply(lambda x: format(x,'.2%'))

df = pd.read_excel('./分组占比模拟数据.xlsx',sheet_name='原始数据')
df['组内指标合计数'] = df.groupby(['事业部'])['指标'].transform('sum')
df.columns = ['事业部','部门','指标','组内指标合计数']
df['组内占比'] = df['指标'] / df['组内指标合计数']
df = df.sort_values(by=['事业部','组内占比'],ascending=[True,False])
df['组内排名（降序）'] = df['指标'].groupby(df['事业部']).rank(method='min',ascending=False).astype(int)
df['组内占比（百分比）'] = df['组内占比'].apply(lambda x: format(x,'.2%'))
df = df.drop(columns = ['组内指标合计数'])
# print(df.info())
df_io = df[['事业部','部门','指标','组内占比（百分比）','组内排名（降序）']]
# 在已有 Excel 文件中生成新的 sheet
writer=pd.ExcelWriter('./python_result.xlsx',mode='a',engine='openpyxl')
df_io.to_excel(writer,sheet_name='group_transform_result', index=False)
writer.save()
writer.close()
print('Excel 文件已生成！！')

tb = pt.PrettyTable()
for col in df_io.columns.values:# 使用 df.columns.values 获取列的名称
    tb.add_column(col, df_io[col])
print(f'处理后的表格如下：\n{tb}')

# 取组内降序排名前五
df_top5 = df[df['组内排名（降序）'] <= 5]
df_top5 = df_top5[['事业部','部门','指标','组内占比（百分比）','组内排名（降序）']].reset_index()
df_top5 = df_top5.drop(labels='index',axis=1)

tb_top5 = pt.PrettyTable()
for col in df_top5.columns.values:
    tb_top5.add_column(col, df_top5[col])
print(f'取组内降序排名前五的表格如下：\n{tb_top5}')

# 取组内占比超过20%
df_over_20pct = df[df['组内占比'] > 0.2]
df_over_20pct = df_over_20pct[['事业部','部门','指标','组内占比（百分比）','组内排名（降序）']].reset_index()
df_over_20pct = df_over_20pct.drop(labels='index',axis=1)

tb_over_20pct = pt.PrettyTable()
for col in df_over_20pct.columns.values:
    tb_over_20pct.add_column(col, df_over_20pct[col])
print(f'取组内占比超过20%的表格如下：\n{tb_over_20pct}')
