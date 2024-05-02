import pandas as pd
from styleframe import StyleFrame, Styler, utils

# 读取数据
df_raw = pd.read_excel("./样例数据.xlsx",sheet_name="raw")


# 清除多余字符
df_raw["货号"] = df_raw["货号"].astype("str")
df_raw["拆分货号"] = df_raw["货号"].str.replace(" ","").replace("\n","/").replace("\r","/")
df_raw["拆分货号"] = df_raw["拆分货号"].astype("str")

# 核心处理步骤：自定义函数，列表化，截取最长的元素，拼接

# 定义一个函数，用于补足货号
# def format_sku(sku_list):
#     # 基数，从第一个数字中删除最后n个数字，n为第二个部分的长度
#     try:
#         base = sku_list[0][:-len(sku_list[1])]  
#         # 构建完整的数字列表
#         numbers = [int(sku_list[0])] + [int(base + part) for part in sku_list[1:]]
#     except:
#         base = sku_list[0]
#         # 构建完整的数字列表
#         numbers = [sku_list[0]] 
#     return numbers


# 定义一个函数，用于补全或保持数字
def format_sku(sku_list,sku_len):
    try:
        # 分割字符串并初始化结果列表和前一个完整数字
        result = []
        prev_full = ""
        
        for sku in sku_list:
            sku = sku.strip()  # 清理空格
            if len(sku) < sku_len and prev_full:  # 如果长度不足且存在前一个完整数字
                # 补全数字
                sku = prev_full[:sku_len-len(sku)] + sku
            result.append(int(sku))  # 添加到结果列表
            prev_full = sku  # 更新前一个完整数字
        
        return result
    except ValueError:
        # 如果转换失败，可能是遇到了特殊字符串，直接返回
        return sku_list


# 处理货号列
for index, row in df_raw.iterrows():
    # 分割货号
    sku_list = row["拆分货号"].split('/')
    # 格式化货号
    formatted_sku = format_sku(sku_list,sku_len=8)
    # 将格式化后的字符串转换回整数
    str_sku_list = [str(num) for num in formatted_sku]
    # 保存处理后的货号列表
    df_raw.at[index, "拆分货号"] = str_sku_list
    
    
# 一行转多列
df = df_raw.explode("拆分货号")
df["提报时间"] = pd.to_datetime(df["提报时间"]).dt.date
print(df)


# 持久化保存
# 美化表格输出格式
# header_style = Styler(
#                         bg_color="blue",
#                         bold=True,
#                         font_size=12,
#                         horizontal_alignment=utils.horizontal_alignments.center,
#                         vertical_alignment=utils.vertical_alignments.center,
#                         )
# content_style = Styler(
#                         shrink_to_fit=True,
#                         font_size=10,
#                         horizontal_alignment=utils.horizontal_alignments.left,
#                         )
# style = Styler(shrink_to_fit=True)

# sf = StyleFrame(df,styler_obj=style)
# sf.apply_column_style(sf.columns, content_style)
# sf.apply_headers_style(header_style)
# writer = sf.to_excel("./真实数据_处理后.xlsx")
# writer.close()
df.to_excel("./样例数据_处理后.xlsx",index=False)
print("表格导出成功！！")