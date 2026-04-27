# 扔掉 SQLite 吧，数据分析该用 DuckDB！

```bash
# 安装所有可选依赖
pip install duckdb[all]
```

## 一、基础用法

```python
import duckdb
import pandas as pd

# 使用 with 语句管理 DuckDB 连接（推荐写法）
with duckdb.connect() as con:
    # 1. 执行 SQL 并获取结果
    # 从DataFrame创建表
    df = pd.DataFrame({
        'product': ['A', 'B', 'C', 'A', 'B'],
        'sales': [100, 200, 150, 120, 180],
        'date': pd.date_range('2024-01-01', periods=5)
    })
    # 注册DataFrame为虚拟表（零拷贝，不复制数据）
    con.register('test', df)
    #  执行 SQL 查询
    result = con.execute("SELECT COUNT(*) FROM test").fetchone()
    print(f"总行数: {result[0]}")  # 输出：总行数: 5

    # 2. 直接查询 CSV / Parquet（添加异常处理，避免文件不存在报错）
    try:
        # 注意：实际使用时请确保 data.csv 存在，或替换为真实文件路径
        df = con.sql("SELECT * FROM 'data.csv' WHERE age > 30").fetchall()
        print(f"查询到 {len(df)} 条符合条件的数据")
        print(df.show())
    except FileNotFoundError:
        print("提示：未找到 data.csv 文件，请检查文件路径是否正确")
    except Exception as e:
        print(f"查询 CSV 时出错：{e}")

# 3. with 块结束后，连接会自动关闭，无需手动调用 con.close()
print("连接已自动关闭")
```

```python
import duckdb
import pandas as pd
import polars as pl

# 与 Pandas / Polars 深度集成
con = duckdb.connect()

# ========== Pandas 互操作 ==========

# Pandas → DuckDB（零拷贝查询）
pandas_df = pd.read_csv('large_file.csv')  # 假设文件存在
con.register('pd_table', pandas_df)
result = con.execute("SELECT * FROM pd_table WHERE value > 100").fetchdf()

# DuckDB → Pandas（聚合结果导出）
aggregated = con.execute("""
    SELECT category, SUM(amount) as total 
    FROM pd_table 
    GROUP BY category
""").fetchdf()  # 返回Pandas DataFrame

# 直接查询 Parquet 文件（无需加载到内存）
# con.execute("SELECT * FROM 'data.parquet' LIMIT 1000").fetchdf()

# ========== Polars 互操作 ==========

# Polars DataFrame → DuckDB
polars_df = pl.DataFrame({
    'x': [1, 2, 3],
    'y': ['a', 'b', 'c']
})
con.register('pl_table', polars_df)

# 查询后转回Polars（零拷贝）
polars_result = con.execute("SELECT * FROM pl_table WHERE x > 1").pl()

# ========== 混合工作流：DuckDB作为查询引擎 ==========

def analyze_with_duckdb(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    使用 DuckDB 对 Pandas DataFrame 执行复杂 SQL 查询
    解决 Pandas 在处理复杂 join 和窗口函数时的性能瓶颈
    """
    con = duckdb.connect()
    con.register('input_data', df)
    return con.execute(query).fetchdf()

# 使用示例：复杂窗口函数（Pandas 中较慢，DuckDB 中极快）
complex_query = """
    WITH monthly_sales AS (
        SELECT 
            DATE_TRUNC('month', sale_date) AS month,
            product_category,
            SUM(amount) AS total_sales,
            COUNT(*) AS transaction_count
        FROM sales
        GROUP BY 1, 2
    ),
    ranked_categories AS (
        SELECT 
            month,
            product_category,
            total_sales,
            ROW_NUMBER() OVER (PARTITION BY month ORDER BY total_sales DESC) AS rank
        FROM monthly_sales
    )
    SELECT * FROM ranked_categories WHERE rank <= 5
    ORDER BY month, rank
"""

con.close()
```



## 二、批量操作与性能优化技巧

```python
import duckdb
import time
import pandas as pd
import polars as pl
import gc

con = duckdb.connect('optimized.db')

# 优化技巧1: 使用 COPY 批量导入（比 INSERT 快 100 倍）
# 从 CSV 直接导入
con.execute("""
    COPY orders FROM 'orders.csv' (HEADER)
""")

# 优化技巧2: 创建索引（仅对点查询有效，分析查询通常不需要）
con.execute("CREATE INDEX idx_user_id ON events(user_id)")

# 优化技巧3: 分区与并行读取 Parquet
con.execute("""
    SELECT * FROM read_parquet('data/*.parquet', hive_partitioning=1)
    WHERE year = 2024 AND month = 3
""")

# 优化技巧4: 内存限制设置（控制内存使用）
con.execute("SET memory_limit = '4GB'")
con.execute("SET threads = 8")  # 控制并行度
conn.execute("SET enable_progress_bar=true")  # 启用进度条

# 优化技巧5: 使用 Prepared Statement 批量插入
data_to_insert = [(i, f'user_{i}', i % 100) for i in range(100000)]
con.executemany("INSERT INTO users VALUES (?, ?, ?)", data_to_insert)

# 优化技巧6：使用 SAMPLE 进行快速探索
sample_result = conn.execute("""
    SELECT * FROM sales USING SAMPLE 10%
""").df()
print("\n采样查询结果:")
print(sample_result.head())

# 性能对比示例
def benchmark_query(con, query, description):
    start = time.time()
    result = con.execute(query).fetchall()
    elapsed = time.time() - start
    print(f"{description}: {elapsed:.3f}s, 返回 {len(result)} 行")
    return elapsed

# 测试窗口函数性能
benchmark_query(con, """
    SELECT user_id, 
           SUM(amount) OVER (PARTITION BY user_id ORDER BY ts ROWS UNBOUNDED PRECEDING)
    FROM events
""", "累计求和窗口函数")


# ====== 综合最佳实践示例 ======

def process_large_data_batched(db_path, query, batch_size=100000):
    """
    批量处理大型数据集的最佳实践函数
    
    参数:
        db_path: 数据库路径
        query: SQL查询语句
        batch_size: 批处理大小
        
    返回:
        处理后的Polars DataFrame
    """
    conn = duckdb.connect(db_path)
    
    try:
        # 设置内存限制
        conn.execute("SET memory_limit='2GB'")
        
        # 执行查询并转换为Polars DataFrame
        result = conn.execute(query).pl(batch_size=batch_size)
        
        return result
    finally:
        # 确保关闭连接
        conn.close()

# 使用示例
result = process_large_data_batched(
    db_path='query_optimization.db',
    query="""
        SELECT 
            region,
            COUNT(*) AS sale_count,
            SUM(amount) AS total_amount,
            AVG(amount) AS avg_amount
        FROM sales
        GROUP BY region
    """,
    batch_size=100000
)
print("\n批量处理函数结果:")
print(result)
```



## 三、实战案例

用户中心的同事向我求助，有两张大表，一张《流失表》作为主表（30多万行），一张《匹配名单表》作为从表（20多万行），需要得到在主表中但不在从表中的数据明细。很简单的一个需求，来看看用 `duckdb` 怎样又快又好地完成任务吧。

```python
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
```



## 四、优缺点与适用场景

| 维度           | **DuckDB**       | **SQLite**       | **Pandas**        | **Spark**           |
| -------------- | ---------------- | ---------------- | ----------------- | ------------------- |
| **核心定位**   | 嵌入式OLAP       | 嵌入式OLTP       | 内存数据处理      | 分布式计算          |
| **存储模型**   | 列式存储         | 行式存储         | 内存对象          | 分布式内存/磁盘     |
| **查询语言**   | SQL              | SQL              | Python API        | SQL/DataFrame API   |
| **最大数据集** | 磁盘大小（流式） | 磁盘大小         | 可用内存          | 集群总存储          |
| **查询性能**   | ⭐⭐⭐⭐⭐（分析）    | ⭐⭐（分析）       | ⭐⭐⭐（复杂查询慢） | ⭐⭐⭐⭐（有启动开销）  |
| **启动延迟**   | 毫秒级           | 毫秒级           | 即时              | 秒级~分钟级         |
| **并发写入**   | 单写多读         | 单写多读         | 无（内存对象）    | 高并发支持          |
| **分布式**     | ❌ 不支持         | ❌ 不支持         | ❌ 不支持          | ✅ 核心特性          |
| **Python集成** | ⭐⭐⭐⭐⭐（原生）    | ⭐⭐⭐（通过驱动）  | ⭐⭐⭐⭐⭐（原生）     | ⭐⭐⭐⭐（PySpark）     |
| **典型场景**   | 本地分析、ETL    | 移动端、配置存储 | 数据探索、原型    | 大数据生产 pipeline |
| **运维复杂度** | 无               | 无               | 无                | 高（需集群管理）    |

| 场景                 | 推荐工具          | 理由                       |
| -------------------- | ----------------- | -------------------------- |
| 本地数据分析（<1TB） | DuckDB            | 性能优越、易于使用         |
| 数据科学原型开发     | DuckDB            | 快速迭代、与Python生态集成 |
| 嵌入式应用数据存储   | SQLite            | 事务处理优化               |
| 应用数据库           | SQLite/PostgreSQL | 成熟的事务支持             |
| 大数据处理（>1TB）   | Apache Spark      | 分布式处理能力             |
| 快速数据探索         | Pandas/DuckDB     | 灵活易用                   |