import pandas as pd

df_raw = pd.read_excel("./加难度的题目.xlsx",sheet_name="可导出版本")

# 将时间转换为datetime类型
df_raw['start_time'] = pd.to_datetime(df_raw['start_time'])
df_raw['end_time'] = pd.to_datetime(df_raw['end_time'])

# 方法一：只能处理跨一年
# # 提取年份
# df_raw['year'] = df_raw['start_time'].dt.year

# # 创建新的数据表
# new_data = []
# for _, row in df_raw.iterrows():
#     if row['start_time'].year != row['end_time'].year:
#         # 跨年的情况，拆分成两行
#         new_data.append([row['ID'], row['start_time'], pd.to_datetime(f"{row['start_time'].year+1}/01/01 00:00:00"), row['start_time'].year])
#         new_data.append([row['ID'], pd.to_datetime(f"{row['start_time'].year+1}/01/01 00:00:00"), row['end_time'], row['end_time'].year])
#     else:
#         new_data.append([row['ID'], row['start_time'], row['end_time'], row['start_time'].year])

# new_df = pd.DataFrame(new_data, columns=['ID', 'start_time', 'end_time', 'year'])

# new_df["duration_seconds"] = (new_df["end_time"] - new_df["start_time"]).dt.total_seconds() # 相差的秒数

# new_df["duration_result"] = pd.to_timedelta(new_df['duration_seconds'], unit='s').apply(lambda x: str(x))

# # 输出结果
# print(new_df)

# 	ID	start_time	end_time	year	duration_seconds	duration_result
# 0	张三	2022-12-01 09:00:00	2023-01-01 00:00:00	2022	2646000.0	30 days 15:00:00
# 1	张三	2023-01-01 00:00:00	2023-01-21 19:30:20	2023	1798220.0	20 days 19:30:20
# 2	张三	2022-12-10 19:00:00	2022-12-21 19:30:20	2022	952220.0000000001	11 days 00:30:20
# 3	张三	2023-01-01 19:30:20	2023-01-31 21:30:29	2023	2599209.0	30 days 02:00:09
# 4	张三	2023-02-01 09:30:20	2023-02-05 10:30:55	2023	349235.0	4 days 01:00:35
# 5	李四	2023-12-01 09:00:00	2023-12-15 19:00:00	2023	1245600.0	14 days 10:00:00
# 6	李四	2023-12-10 19:00:00	2023-12-21 19:30:20	2023	952220.0000000001	11 days 00:30:20
# 7	李四	2023-12-22 09:00:00	2023-12-25 10:15:08	2023	263708.0	3 days 01:15:08
# 8	王五	2023-12-01 09:00:00	2023-12-01 14:15:05	2023	18905.0	0 days 05:15:05
# 9	王五	2023-12-10 19:00:00	2023-12-20 19:30:20	2023	865820.0	10 days 00:30:20



# 方法二：可以处理跨多年
# 处理跨年情况
new_rows = []
for index, row in df_raw.iterrows():
    start_year = row['start_time'].year
    end_year = row['end_time'].year
    if start_year != end_year:
        # 添加第一段时间
        new_rows.append([row['ID'], row['start_time'], pd.Timestamp(f"{start_year+1}-01-01 00:00:00"), start_year])
        # 添加中间段时间
        for year in range(start_year+1, end_year):
            new_rows.append([row['ID'], pd.Timestamp(f"{year}-01-01 00:00:00"), pd.Timestamp(f"{year+1}-01-01 00:00:00"), year])
        # 添加最后一段时间
        new_rows.append([row['ID'], pd.Timestamp(f"{end_year}-01-01 00:00:00"), row['end_time'], end_year])
    else:
        new_rows.append([row['ID'], row['start_time'], row['end_time'], start_year])

# 创建新的 DataFrame
new_df = pd.DataFrame(new_rows, columns=['ID', 'start_time', 'end_time', 'year'])

# 输出结果
print(new_df)

#    ID          start_time            end_time  year
# 0  张三 2022-12-01 09:00:00 2023-01-01 00:00:00  2022
# 1  张三 2023-01-01 00:00:00 2023-01-21 19:30:20  2023
# 2  张三 2022-12-10 19:00:00 2022-12-21 19:30:20  2022
# 3  张三 2023-01-01 19:30:20 2023-01-31 21:30:29  2023
# 4  张三 2023-02-01 09:30:20 2023-02-05 10:30:55  2023
# 5  李四 2023-12-01 09:00:00 2023-12-15 19:00:00  2023
# 6  李四 2023-12-10 19:00:00 2023-12-21 19:30:20  2023
# 7  李四 2023-12-22 09:00:00 2023-12-25 10:15:08  2023
# 8  王五 2023-12-01 09:00:00 2023-12-01 14:15:05  2023
# 9  王五 2023-12-10 19:00:00 2023-12-20 19:30:20  2023