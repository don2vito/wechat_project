import pandas as pd
import warnings
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
import time

def deal(data):
    # 删除带有空值的行，只要有一个空值，就删除整行，并生成列表
    return data.dropna().tolist()

def data_transform():
    # 导入数据并进行条件过滤
    df = pd.read_excel('./销售基础表查询.xlsx', sheet_name='销售基础表查询', header=0)
    # print(df.head())
    # print(df.shape)
    bool_content = ((df['实销数量'] > 0) & (df['实销金额'] > 0))
    df = df[bool_content]
    # print(df.head())
    print('df: {}'.format(df.shape))
    # 选择需要的数据字段
    df2 = df[['单据号', '商品']]
    print('df2: {}'.format(df2.shape))
    # 数据整合 —— 唯一单据号对应商品
    df3 = pd.DataFrame([(i, df2[df2['单据号'] == i]['商品'].tolist()) for i in df2['单据号'].unique()])
    print('df3: {}'.format(df3.shape))
    # 生成购物篮对应商品列表
    # shopping_lists = []
    # for shopping_list in df3[1]:
    #     shopping_lists.append(shopping_list)
    # shopping_df = pd.DataFrame(shopping_lists)
    # print(shopping_df.head(20))
    # 剔除数据中的空值（ apply ）
    # df_arr = shopping_df.apply(deal, axis=1).tolist()
    # print('df_arr: {}'.format(len(df_arr)))
    # print(df_arr[:21])
    df_arr = df3[1].tolist()
    print('df_arr: {}'.format(len(df_arr)))
    # 调用模型
    te = TransactionEncoder()
    df_tf = te.fit_transform(df_arr)
    # 生成数据集
    df4 = pd.DataFrame(df_tf, columns=te.columns_)
    print('df4: {}'.format(df4.shape))
    # print(df4.head(20))
    # 返回数据
    return df4

def association_apriori(data,min_support=0.5,use_colnames=True,metric='lift',min_threshold=1):
    # 设置支持度来选择频繁项集
    frequent_itemsets = apriori(data, min_support=min_support, use_colnames=use_colnames)
    frequent_itemsets.sort_values(by='support', ascending=False, inplace=True)
    print(frequent_itemsets)
    # 计算规则（指定不同的衡量标准和最小阈值）
    association_rule = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    association_rule.sort_values(by='leverage', ascending=False, inplace=True)
    print(association_rule)
    # 根据业务逻辑调整阈值
    bool_content = ((association_rule['lift'] > 1.25) & (association_rule['confidence'] > 0.5))
    association_rule = association_rule[bool_content]
    print(association_rule)

if __name__ == '__main__':
    pd.set_option('display.max_columns', 100)
    pd.set_option('precision', 3)

    warnings.filterwarnings('ignore')

    t1 = time.time()
    # 步骤一：数据转换
    data = data_transform()
    # 步骤二：进行 Apriori 关联分析
    association_apriori(data,min_support=0.005)
    t2 = time.time()
    print('运行共耗时: {:.2f}秒'.format(t2 - t1))

    # ==================================================================================================================
    # ==================================================================================================================
    # df: (34121, 46)
    # df2: (34121, 2)
    # df3: (10967, 2)
    # df_arr: 10967
    # df4: (10967, 1472)
    # ==================================================================================================================
    # ==================================================================================================================
    #      support              itemsets
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
    # ==================================================================================================================
    # ==================================================================================================================
    #           antecedents         consequents  antecedent support  \
    # 0  (Q62211104|正装西服下衣)  (Q62210104|正装西服上衣)               0.008
    # 1  (Q62210104|正装西服上衣)  (Q62211104|正装西服下衣)               0.008
    #
    #    consequent support  support  confidence    lift  leverage  conviction
    # 0               0.008    0.006       0.741  95.629     0.006       3.834
    # 1               0.008    0.006       0.741  95.629     0.006       3.834
    # ==================================================================================================================
    # ==================================================================================================================
    #           antecedents         consequents  antecedent support  \
    # 0  (Q62211104|正装西服下衣)  (Q62210104|正装西服上衣)               0.008
    # 1  (Q62210104|正装西服上衣)  (Q62211104|正装西服下衣)               0.008
    #
    #    consequent support  support  confidence    lift  leverage  conviction
    # 0               0.008    0.006       0.741  95.629     0.006       3.834
    # 1               0.008    0.006       0.741  95.629     0.006       3.834
    # 运行共耗时: 75.80秒
    # ==================================================================================================================
    # ==================================================================================================================
    # 字段说明
    # antecedents：规则先导项
    # consequents：规则后继项
    # antecedent support：规则先导项支持度
    # consequent support：规则后继项支持度
    # support：规则支持度 （前项后项并集的支持度）
    # confidence：规则置信度 （规则置信度：规则支持度support / 规则先导项）
    # lift：规则提升度，表示含有先导项条件下同时含有后继项的概率，与后继项总体发生的概率之比。
    # leverage：规则杠杆率，表示当先导项与后继项独立分布时，先导项与后继项一起出现的次数比预期多多少。
    # conviction：规则确信度，与提升度类似，但用差值表示