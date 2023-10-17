from rapidfuzz import fuzz,process
import pandas as pd 
import tqdm
from faker import Faker 


# process 模块主要用在字符串列表 choices 中查找最相似字符串或计算相似度
# 1. process.cdist 查询为字符串列表，计算两个列表中字符串的相似度
# process.cdist(queries, choices, *, scorer=<cyfunction ratio>, processor=None, score_cutoff=None, dtype=None, workers=1, **kwargs)

# 2. process.extract 查询为字符串，返回按照相似度排序的结果；返回列表的元素类型是含有 3 个元素的元组。第一个值为 choices 中元素；第二个值一般是相似度，但取值根据 scorer 不同形式上会有不同（当 scorer 为 string_metric.levenshtein 时，0 表示完美匹配）；第三个元素是列表索引或者字典的 key
# process.extract(query, choices, *, scorer=<cyfunction WRatio>, processor=<cyfunction default_process>, limit=5, score_cutoff=None, **kwargs)
choices = ["邻家饭香", "南京东郊宾馆", "兔宝宝(TUBAO)", "含羞草(MIMOSA)"]
result_extract = process.extract("TUBAO兔宝宝", choices, limit=2)
print(f"提取多条数据的结果是：{result_extract}")


# 3. process.extract_iter 查询为字符串，返回迭代器，此时并未排序，顺序与原 choices 一致，结果形式同样是元组
# process.extract_iter(query, choices, *, scorer=<cyfunction WRatio>, processor=<cyfunction default_process>, score_cutoff=None, **kwargs)

# 4. process.extractOne 返回最佳匹配结果
choices = ["邻家饭香", "南京东郊宾馆", "兔宝宝(TUBAO)", "含羞草(MIMOSA)"]
result_extractOne = process.extractOne("TUBAO兔宝宝", choices)
print(f"提取单条数据的结果是：{result_extractOne}")



# fuzz 模块
# 1. token_ratio 返回 token_set_ratio 和 token_sort_ratio 二者值最大的结果，运行速度比分别调用再比较要快
# 2. partial_token_ratio 返回 partial_token_set_ratio 和 partial_token_sort_ratio 二者值最大的结果，运行速度比分别调用再比较要快很多


# 简单匹配
result_ratio = int(round(fuzz.ratio("TUBAO兔宝宝", "兔宝宝(TUBAO)"),0))
print(f"简单匹配的结果是：{result_ratio}")

# 非完全匹配
result_partial_ratio = int(round(fuzz.partial_ratio("TUBAO兔宝宝", "兔宝宝(TUBAO)"),0))
print(f"非完全匹配的结果是：{result_partial_ratio}")

# 忽略顺序匹配
result_token_sort_ratio = int(round(fuzz.token_sort_ratio("TUBAO兔宝宝", "兔宝宝(TUBAO)"),0))
print(f"忽略顺序匹配的结果是：{result_token_sort_ratio}")

# 去重子集匹配
result_token_set_ratio = int(round(fuzz.token_set_ratio("TUBAO兔宝宝", "兔宝宝(TUBAO)"),0))
print(f"去重子集匹配的结果是：{result_token_set_ratio}")




# 案例一：品牌名称匹配（多匹少）
def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    s = df_2[key2].tolist()

    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['匹配列'] = m

    m2 = df_1['匹配列'].apply(lambda x: [i[0] for i in x if i[1] >= threshold][0] if len([i[0] for i in x if i[1] >= threshold]) > 0 else '')
    df_1['匹配列'] = m2

    return df_1


df_1 = pd.read_excel('./品牌清单.xlsx',sheet_name="多")
df_2 = pd.read_excel('./品牌清单.xlsx',sheet_name="少")
df_result = fuzzy_merge(df_1, df_2, '品牌名称', '品牌名', threshold=90, limit=2)
print(df_result)





# 案例二：电商长尾词名称匹配品类
df_3 = pd.read_excel('./SKU清单.xlsx',sheet_name="data")
df_4 = pd.read_excel('./SKU清单.xlsx',sheet_name="param")
df_result2 = fuzzy_merge(df_3, df_4, '品名', '类目', threshold=30, limit=2)
print(df_result2)