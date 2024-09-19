import pandas as pd
import numpy as np

df = pd.read_csv('./customers_data.csv')
df['付款时间'] = pd.to_datetime(df['付款时间'])
df['付款年月'] = df['付款时间'].dt.strftime('%Y-%m')
# print(df.sample(10))

# 月份列表
month_list = list(df['付款年月'].unique())

# 初始化存储留存数据的列表，个数为 len(month_list) - 1
retention_data = [[] for _ in range(len(month_list) - 1)]

# 存储每月新增的客户数
monthly_increase = {} # 用字典存储，格式输出漂亮些，也有助于添加进 DataFrame 中

for i in range(0, len(month_list)):
    
    # 筛选出 month_list 中的每月消费，并统计客户数量
    print(f'下面统计: {month_list[i]} 的新增情况...')
    current_data = df[ df['付款年月']==month_list[i] ]
    current_clients = current_data['脱敏客户ID'].unique()
    
    # =========================== 统计新增情况 ==================================
    # 跳过数据集中的第一个月，因为没有历史数据来验证该客户是否为新增客户
    if i == 0:
        print(f'{month_list[i]} 是第一个月，无需验证客户是否为新增客户。')
        new_clients_num = len(current_clients)
        print(f'该月的新增用户数为：{new_clients_num}')
        monthly_increase[month_list[i]] = new_clients_num
        
    else:
        # 筛选该月（current_month）之前的所有历史消费记录
        history_month = month_list[:i]
        print(f'{month_list[i]} 的历史年月为：{history_month}')
        history_data = df[ df['付款年月'].isin(history_month) ]
        # 筛选未在历史消费记录中出现过的新增客户
        new_users = np.setdiff1d(current_data['脱敏客户ID'], history_data['脱敏客户ID'])
        print(f'相较于历史年月，该月的新增客户数为：{len(new_users)}')
        monthly_increase[month_list[i]] = len(new_users)
        
    # =========================== 统计留存情况 ==================================
    print('-'*50)
    print('下面统计该月之后的每个月的留存情况...')
    # print('下面统计该月之后的每个月的客户平均消费金额情况...')
    for j in range(i+1, len(month_list)):
        next_month_data = df[ df['付款年月']==month_list[j]]
        # 统计各群的用户平均消费金额
        # user_purchase = next_month_data.groupby('脱敏客户ID')['支付金额'].agg('mean')
        # 统计既出现在该月，又出现在下个月的用户
        next_month_retain = np.intersect1d(current_data['脱敏客户ID'], next_month_data['脱敏客户ID'])
        print(f'{month_list[j]} 的留存人数：{len(next_month_retain)}')
        # print(f'{month_list[j]} 的留存人数：{len(next_month_retain)}，客户平均消费金额：{round(user_purchase.mean())}')
        # next_month_price_avg = round(user_purchase.mean())
        
        # 根据时间间隔存储数据
        interval = j - i - 1
        retention_data[interval].append(len(next_month_retain))
        # retention_data[interval].append(next_month_price_avg)
    
# 在每个列表末尾补 0 以确保所有列表长度都为 len(month_list)
for idx in range(len(retention_data)):
    # 补齐 0，确保每个列表长度为 len(month_list)
    while len(retention_data[idx]) < len(month_list):
        retention_data[idx].append(0)

# 打印结果，命名格式修改为 plus_1, plus_2 等
for idx, data in enumerate(retention_data, start=1):
    # print(f"plus_{idx} = {data}")
    var_name = f"plus_{idx}"
    globals()[var_name] = data  # 动态创建变量
    print(f"{var_name} = {data}")  # 打印输出
print('\n')
# 下面统计: 2023-09 的新增情况...
# 2023-09 是第一个月，无需验证客户是否为新增客户。
# 该月的新增用户数为：2031
# --------------------------------------------------
# 下面统计该月之后的每个月的留存情况...
# 2023-10 的留存人数：252
# 2023-11 的留存人数：216
# 2023-12 的留存人数：163
# 2024-01 的留存人数：156
# 2024-02 的留存人数：164
# 下面统计: 2023-10 的新增情况...
# 2023-10 的历史年月为：['2023-09']
# 相较于历史年月，该月的新增客户数为：7043
# --------------------------------------------------
# 下面统计该月之后的每个月的留存情况...
# 2023-11 的留存人数：623
# 2023-12 的留存人数：491
# 2024-01 的留存人数：488
# 2024-02 的留存人数：491
# 下面统计: 2023-11 的新增情况...
# 2023-11 的历史年月为：['2023-09', '2023-10']
# 相较于历史年月，该月的新增客户数为：4732
# --------------------------------------------------
# 下面统计该月之后的每个月的留存情况...
# 2023-12 的留存人数：637
# 2024-01 的留存人数：562
# 2024-02 的留存人数：486
# 下面统计: 2023-12 的新增情况...
# 2023-12 的历史年月为：['2023-09', '2023-10', '2023-11']
# 相较于历史年月，该月的新增客户数为：4979
# --------------------------------------------------
# 下面统计该月之后的每个月的留存情况...
# 2024-01 的留存人数：821
# 2024-02 的留存人数：636
# 下面统计: 2024-01 的新增情况...
# 2024-01 的历史年月为：['2023-09', '2023-10', '2023-11', '2023-12']
# 相较于历史年月，该月的新增客户数为：5110
# --------------------------------------------------
# 下面统计该月之后的每个月的留存情况...
# 2024-02 的留存人数：909
# 下面统计: 2024-02 的新增情况...
# 2024-02 的历史年月为：['2023-09', '2023-10', '2023-11', '2023-12', '2024-01']
# 相较于历史年月，该月的新增客户数为：7101
# --------------------------------------------------
# 下面统计该月之后的每个月的留存情况...
# plus_1 = [252, 623, 637, 821, 909, 0]
# plus_2 = [216, 491, 562, 636, 0, 0]
# plus_3 = [163, 488, 486, 0, 0, 0]
# plus_4 = [156, 491, 0, 0, 0, 0]
# plus_5 = [164, 0, 0, 0, 0, 0]
    
print(monthly_increase)
# {'2023-09': 2031, '2023-10': 7043, '2023-11': 4732, '2023-12': 4979, '2024-01': 5110, '2024-02': 7101}

# DataFrame 的索引
result_index = list(monthly_increase.keys()) 
# 当月新增
current_month_increase = list(monthly_increase.values())

data = {'当月新增': current_month_increase,
       '+1月': plus_1, '+2月': plus_2, 
       '+3月': plus_3, '+4月': plus_4, '+5月': plus_5}

result = pd.DataFrame(data, index=result_index, columns=list(data.keys()))
print(result)
#          当月新增  +1月  +2月  +3月  +4月  +5月
# 2023-09  2031  252  216  163  156  164
# 2023-10  7043  623  491  488  491    0
# 2023-11  4732  637  562  486    0    0
# 2023-12  4979  821  636    0    0    0
# 2024-01  5110  909    0    0    0    0
# 2024-02  7101    0    0    0    0    0


# 留存率表计算
# 求比率
# iloc：行的全部，列的第二行到最后一行
# axis=0: 对横行的 +1~+5月的留存客户数都进行除以当月新增的操作
final = result.divide(result['当月新增'], axis=0).iloc[:, 1:]
final['当月新增'] = result['当月新增']

# 调整列顺序
final = final[['当月新增', '+1月', '+2月', '+3月', '+4月', '+5月']]
final[['+1月', '+2月', '+3月', '+4月', '+5月']] = final[['+1月', '+2月', '+3月', '+4月', '+5月']].applymap(lambda x: str(round(x*100))+'%' )
final.replace('0%', '-', inplace=True)
print(final)
#          当月新增  +1月  +2月  +3月 +4月 +5月
# 2023-09  2031  12%  11%   8%  8%  8%
# 2023-10  7043   9%   7%   7%  7%   -
# 2023-11  4732  13%  12%  10%   -   -
# 2023-12  4979  16%  13%    -   -   -
# 2024-01  5110  18%    -    -   -   -
# 2024-02  7101    -    -    -   -   -