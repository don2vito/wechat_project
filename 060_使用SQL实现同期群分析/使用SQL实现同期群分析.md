# 使用 SQL 实现同期群分析

[TOC]

## 一、同期群分析的定义

> **同期群分析**（Cohort Analysis）是一种通过“纵横”结合对用户分群的细分类型分析的方法：
>
> - **横向上**——分析同期群随着周期推移而发生的变化
> - **纵向上**——分析在生命周期相同阶段的群组之间的差异

**同期群**指的是同一时期的群体，可以是同一天注册的用户、同一天第一次发生付费行为的用户等。

**周期的指标变化**是指用户在一定周期内的留存率、付费率等指标。

> 同期群分析包含三个核心的元素：
>
> - **客户首次行为时间**：这是划分同期群体的基点
>
> - **时间周期维度**：比如 N 日留存率、N 日转化率中的 N 日，一般即为 +N 日、+N 月
>
> - **变化的指标**：比如注册转化率、付款转化率、留存率等指标

同期群分析给到更加细致的衡量指标，可以实时监控真实的用户行为、衡量用户价值，并为营销方案的优化和改进提供支撑，避免“被平均”的虚荣数据。



## 二、SQL 步骤

下面我使用 PostgreSQL 拆分步骤来实现基于首单日期的用户留存率同期群报表，**每一步骤都是在前一步骤的基础上进行再加工**，这在代码中的子查询中也得到体现，理清了思路就会发现其实很简单。

> 重点有以下几点：
>
> - 统计出每个用户的**首单时间**
> - 计算首单时间和实际下单时间的**日期差**
> - 对于付费用户数需要**去重统计**
> - 注意字段**格式的转换**

### 1. 查看数据

```SQL
-- 0. 查看数据

SELECT * FROM "日志" LIMIT 10;
```

![](https://files.mdnice.com/user/1655/c7d957d9-0ba7-4dc7-84e4-4582b9db161b.png)

### 2. 根据 uid 、年月聚合用户人数

```SQL
-- 1. 根据 uid 、年月聚合用户人数

SELECT
	"日志".uid,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' ) AS 年月,
	min(to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )) OVER(PARTITION BY "日志".uid) AS 首次付费年月
FROM
	"日志" 
GROUP BY
	"日志".uid,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )
	ORDER BY "日志".uid;
```

![](https://files.mdnice.com/user/1655/f011054e-415a-49ec-a812-20dfacdc8cf5.png)

### 3. 计算年月的差额（天数）

```SQL
-- 2. 计算年月的差额（天数）

SELECT *,to_date(t.年月,'YYYY-MM') - to_date(t.首次付费年月,'YYYY-MM') AS 天数差额
FROM (SELECT
	"日志".uid,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' ) AS 年月,
	min(to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )) OVER(PARTITION BY "日志".uid) AS 首次付费年月
FROM
	"日志" 
GROUP BY
	"日志".uid,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )
	ORDER BY "日志".uid) AS t;
```

![](https://files.mdnice.com/user/1655/2d381faa-eea9-4596-b91b-268fdb0f0d87.png)

### 4. 计算年月的差额（月数）

```SQL
-- 3. 计算年月的差额（月数）

SELECT t.*,
(case when t."天数差额" <= 30 then '首月' 
	   when t."天数差额" <= 60 then '+1月'
		 when t."天数差额" <= 90 then '+2月' 
		 when t."天数差额" <= 120 then '+3月'
		 when t."天数差额" <= 150 then '+4月'
		 else NULL
		 END)  AS 月差额
FROM (SELECT *,to_date(t.年月,'YYYY-MM') - to_date(t.首次付费年月,'YYYY-MM') AS 天数差额
FROM (SELECT
	"日志".uid,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' ) AS 年月,
	min(to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )) OVER(PARTITION BY "日志".uid) AS 首次付费年月
FROM
	"日志" 
GROUP BY
	"日志".uid,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )
	ORDER BY "日志".uid) AS t) AS t;
```

![](https://files.mdnice.com/user/1655/795e08db-bd91-40a1-af1c-029aeb44e4f8.png)

### 5. 透视（根据 uid 、首次付费年月去透视年月差额的用户人数）

```SQL
-- 4. 透视（根据 uid 、首次付费年月去透视年月差额的用户人数）

SELECT t.首次付费年月,
count(distinct case when t.年月差额 = 0 then t.uid else NULL end) AS 首月,
count(distinct case when t.年月差额 = 1 then t.uid else NULL end) AS "+1月",
count(distinct case when t.年月差额 = 2 then t.uid else NULL end) AS "+2月",
count(distinct case when t.年月差额 = 3 then t.uid else NULL end) AS "+3月",
count(distinct case when t.年月差额 = 4 then t.uid else NULL end) AS "+4月"
FROM (SELECT * FROM (SELECT *,round((to_date(t.年月,'YYYY-MM') - to_date(t.首次付费年月,'YYYY-MM')) / 30,0) AS 年月差额
FROM (SELECT
	"日志".uid:: text,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' ) AS 年月,
	min(to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )) OVER(PARTITION BY "日志".uid) AS 首次付费年月
FROM
	"日志" 
GROUP BY
	"日志".uid,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )
	ORDER BY "日志".uid) AS t) AS t) AS t
	GROUP BY t.首次付费年月;
```

![](https://files.mdnice.com/user/1655/a0bf278e-211e-4700-b978-05d81408ca4a.png)

### 6. 计算留存率

```SQL
-- 5. 计算留存率

SELECT t.首次付费年月,t.首月,
round((t."+1月"::numeric / t.首月::numeric) * 100,2)::text || '%' AS "1月后",
round((t."+2月"::numeric / t.首月::numeric) * 100,2)::text || '%' AS "2月后",
round((t."+3月"::numeric / t.首月::numeric) * 100,2)::text || '%' AS "3月后",
round((t."+4月"::numeric / t.首月::numeric) * 100,2)::text || '%' AS "4月后"
FROM(SELECT t.首次付费年月,
count(distinct case when t.年月差额 = 0 then t.uid else NULL end) AS 首月,
count(distinct case when t.年月差额 = 1 then t.uid else NULL end) AS "+1月",
count(distinct case when t.年月差额 = 2 then t.uid else NULL end) AS "+2月",
count(distinct case when t.年月差额 = 3 then t.uid else NULL end) AS "+3月",
count(distinct case when t.年月差额 = 4 then t.uid else NULL end) AS "+4月"
FROM (SELECT * FROM (SELECT *,round((to_date(t.年月,'YYYY-MM') - to_date(t.首次付费年月,'YYYY-MM')) / 30,0) AS 年月差额
FROM (SELECT
	"日志".uid:: text,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' ) AS 年月,
	min(to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )) OVER(PARTITION BY "日志".uid) AS 首次付费年月
FROM
	"日志" 
GROUP BY
	"日志".uid,
	to_char( to_date( "日志"."日期", 'YYYY-MM' ), 'YYYY-MM' )
	ORDER BY "日志".uid) AS t) AS t) AS t
	GROUP BY t.首次付费年月) AS t;
```

![](https://files.mdnice.com/user/1655/a01b46ac-5377-4230-8e53-834855edd990.png)

