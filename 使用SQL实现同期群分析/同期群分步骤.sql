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
	
	
-- 3. 计算年月的差额（月数）

SELECT t.*,(case when t."天数差额" <= 30 then '首月' 	   when t."天数差额" <= 60 then '+1月'
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