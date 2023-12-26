
-- 步骤一：比较基准点的获取

WITH a_t AS (
		SELECT
			"跨年重复时间段的时长问题"."ID",
			"跨年重复时间段的时长问题"."year",
			"跨年重复时间段的时长问题".start_time,
			"跨年重复时间段的时长问题".end_time,
			MAX ( "跨年重复时间段的时长问题".end_time ) OVER ( PARTITION BY "跨年重复时间段的时长问题"."ID", "跨年重复时间段的时长问题"."year" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING ) AS std_edt 
		FROM
		"跨年重复时间段的时长问题" 
	) ,

-- 	步骤二：重复部分的判断及处理

b_t AS (
SELECT a_t."ID",a_t."year",
CASE
		WHEN std_edt IS NULL THEN start_time 
		WHEN 
			(
			DATE_PART( 'day', start_time :: TIMESTAMP - std_edt :: TIMESTAMP ) * 24 * 60 * 60 + DATE_PART( 'hour', start_time :: TIMESTAMP - std_edt :: TIMESTAMP ) 
			 * 60 * 60 + DATE_PART( 'minute', start_time :: TIMESTAMP - std_edt :: TIMESTAMP ) 
			 * 60 + DATE_PART( 'second', start_time :: TIMESTAMP - std_edt :: TIMESTAMP ))> 0 THEN
			start_time ELSE std_edt :: TIMESTAMP + '1 day' 
		END AS start_time,
		end_time 
	FROM a_t
	) ,
	
-- 步骤三：计算结果
	
c_t AS ( SELECT b_t."ID",b_t."year",start_time,end_time,
(
			DATE_PART( 'day',end_time :: TIMESTAMP - start_time :: TIMESTAMP ) * 24 * 60 * 60 + DATE_PART( 'hour', end_time :: TIMESTAMP - start_time :: TIMESTAMP ) 
			 * 60 * 60 + DATE_PART( 'minute', end_time :: TIMESTAMP - start_time :: TIMESTAMP ) 
			 * 60 + DATE_PART( 'second', end_time:: TIMESTAMP - start_time :: TIMESTAMP )) AS diff

FROM b_t
) ,

d_t AS (
SELECT c_t."ID",c_t."year",SUM(CASE WHEN diff > 0 THEN diff + 60 * 60 * 24 ELSE NULL END) AS All_seconds
FROM c_t
GROUP BY c_t."ID",c_t."year"
) ,

e_t AS (
SELECT d_t."ID",d_t."year",All_seconds,All_seconds::INT / (24 * 60 * 60) AS days,
(All_seconds::INT / (60 * 60)) % 24 AS hours,
(All_seconds::INT / 60 % 60) AS minutes,
(All_seconds::INT % 60) AS seconds
FROM d_t
)




SELECT * FROM e_t
