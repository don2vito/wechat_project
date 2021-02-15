import pandas as pd
import warnings
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules


pd.set_option('display.max_columns', 100)
pd.set_option('precision', 3)

warnings.filterwarnings('ignore')

# 方法一：使用 mlxtend 库
# 数据转换
df = pd.read_excel('./销售基础表查询.xlsx',sheet_name='销售基础表查询',header=0)
# print(df.head())
# print(df.shape)
bool_content = ((df['实销数量'] > 0) & (df['实销金额'] > 0))
df = df[bool_content]
# print(df.head())
# print(df.shape)
df2 = df[['单据号','商品']]
# print(df2.shape)
# df2.to_excel('./cleaned_sales_table.xlsx',sheet_name='cleamed_sales_table',index=False,columns=['单据号','商品'],encoding='utf-8')
# df3 = df2.join(pd.get_dummies(df2['商品']))
# df3.drop(['商品'],axis=1,inplace=True)
# df3 = pd.get_dummies(df2['商品'])
# print(df3.head())
# print(df3.shape)

df4 = pd.DataFrame([(i,df2[df2['单据号'] == i]['商品'].tolist()) for i in df2['单据号'].unique()])
shopping_lists = []
for shopping_list in df4[1]:
    shopping_lists.append(shopping_list)
shopping_df = pd.DataFrame(shopping_lists)
# print(shopping_df)
def deal(data):
	return data.dropna().tolist()
df_arr = shopping_df.apply(deal,axis=1).tolist()
te = TransactionEncoder()
df_tf = te.fit_transform(df_arr)
df5 = pd.DataFrame(df_tf,columns=te.columns_)
# print(df5)
'''
# print(df3[['1010-0004|单夹克','1010-0005|单夹克']])
# print(df3.iloc[:,1:3])

col_names = df3.columns
# print(col_names[1:])
col_selected = []
for col_name in col_names[1:]:
    col_selected.append(col_name)
df3 = df3[col_selected]
# print(df3)
'''
# 设置支持度来选择频繁项集
frequent_itemsets = apriori(df5,min_support=0.005, use_colnames=True)
frequent_itemsets.sort_values(by='support',ascending=False,inplace=True)
print(frequent_itemsets)

# support              itemsets
# 85     0.025    (P91404042|针织短袖T恤)
# 13     0.025       (D71303009|休闲裤)
# 109    0.024    (P91636117|针织长袖T恤)
# 83     0.023    (P91404041|针织短袖T恤)
# 49     0.021       (P91303005|休闲裤)
# ..       ...                   ...
# 26     0.005    (D71404070|针织短袖T恤)
# 146    0.005    (Z52636111|针织长袖T恤)
# 31     0.005    (D71525319|休闲短袖衬衫)
# 74     0.005  (P91404027-J|针织短袖T恤)
# 90     0.005    (P91404049|针织短袖T恤)
#
# [154 rows x 2 columns]

# 计算规则（指定不同的衡量标准和最小阈值）
association_rule = association_rules(frequent_itemsets,metric='lift',min_threshold=1)
association_rule.sort_values(by='leverage',ascending=False,inplace=True)
print(association_rule)

#           antecedents         consequents  antecedent support  \
# 0  (Q62210104|正装西服上衣)  (Q62211104|正装西服下衣)               0.008
# 1  (Q62211104|正装西服下衣)  (Q62210104|正装西服上衣)               0.008
#
#    consequent support  support  confidence    lift  leverage  conviction
# 0               0.008    0.006       0.741  95.629     0.006       3.834
# 1               0.008    0.006       0.741  95.629     0.006       3.834

# 根据业务逻辑调整阈值
bool_content = ((association_rule['lift'] > 1.25) & (association_rule['confidence'] > 0.5))
association_rule = association_rule[bool_content]
print(association_rule)

#           antecedents         consequents  antecedent support  \
# 0  (Q62210104|正装西服上衣)  (Q62211104|正装西服下衣)               0.008
# 1  (Q62211104|正装西服下衣)  (Q62210104|正装西服上衣)               0.008
#
#    consequent support  support  confidence    lift  leverage  conviction
# 0               0.008    0.006       0.741  95.629     0.006       3.834
# 1               0.008    0.006       0.741  95.629     0.006       3.834

# antecedents：规则先导项
#
# consequents：规则后继项
#
# antecedent support：规则先导项支持度
#
# consequent support：规则后继项支持度
#
# support：规则支持度 （前项后项并集的支持度）
#
# confidence：规则置信度 （规则置信度：规则支持度support / 规则先导项）
#
# lift：规则提升度，表示含有先导项条件下同时含有后继项的概率，与后继项总体发生的概率之比。
#
# leverage：规则杠杆率，表示当先导项与后继项独立分布时，先导项与后继项一起出现的次数比预期多多少。
#
# conviction：规则确信度，与提升度类似，但用差值表示


'''
# 方法二：使用 apriori 库
# 数据转换
df4 = pd.DataFrame([df[df['单据号'] == i]['商品'].tolist() for i in df['单据号'].unique()])
print(df4.shape)
data_list = []
for i in df4[1]:
    data_list.append(i)
print(data_list[:5])

# 调用库
itemsets,rules = apriori(data_list,min_support=0.5,min_confidence=1)
print(itemsets)
print(rules)
'''