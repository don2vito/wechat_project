SELECT
	c_tb.uid,
	c_tb.时间段 
FROM
	(
SELECT
	b_tb.uid,
	b_tb.时间段,
	COUNT ( b_tb.时间段 ),
	DENSE_RANK () OVER ( PARTITION BY b_tb.uid ORDER BY COUNT ( b_tb.时间段 ) DESC ) AS 降序排序 
FROM
	(
SELECT
	*,
CASE
	
	WHEN a_tb.hour_str >= '00' 
	AND a_tb.hour_str < '06' THEN
	'凌晨' 
WHEN a_tb.hour_str >= '06' 
AND a_tb.hour_str < '12' THEN
'上午' 
WHEN a_tb.hour_str >= '12' 
AND a_tb.hour_str < '18' THEN
'下午' 
WHEN a_tb.hour_str >= '18' 
AND a_tb.hour_str < '24' THEN
'夜晚' ELSE NULL 
END AS 时间段 
FROM
	(
	SELECT
		"2题data2".uid,
		"2题data2".occur_date,
		to_char( "2题data2".first_time, 'HH24' ) AS hour_str,
		DENSE_RANK () OVER ( PARTITION BY "2题data2".uid ORDER BY "2题data2".occur_date DESC ) AS rank_desc 
	FROM
		"2题data2" 
	ORDER BY
		"2题data2".uid,
		"2题data2".occur_date 
	) AS a_tb 
WHERE
	a_tb.rank_desc <= 4 
ORDER BY
	a_tb.uid,
	a_tb.occur_date 
	) AS b_tb 
GROUP BY
	b_tb.uid,
	b_tb.时间段 
ORDER BY
	b_tb.uid,
	b_tb.时间段 
	) AS c_tb 
WHERE
c_tb.降序排序 = 1;