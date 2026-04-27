import duckdb
import pandas as pd

table_main = pd.read_excel("./流失.xlsx")
table_sub = pd.read_excel("./匹配名单.xlsx")

with duckdb.connect() as con:
    con.register('main', table_main)
    con.register('sub', table_sub)
    
    result = con.execute('SELECT a.*,b.cust_id AS "匹配" FROM main AS a LEFT JOIN sub AS b ON a."客户编码" = b.cust_id WHERE b.cust_id IS NULL').df()
    
    print(result.head())
    
    result.to_excel("./在流失主表中剔除匹配名单.xlsx",index=False)
print("数据处理完成！")