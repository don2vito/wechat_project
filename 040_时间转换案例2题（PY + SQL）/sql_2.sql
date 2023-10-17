SELECT
	c_tb.uid,
	c_tb.ʱ��� 
FROM
	(
SELECT
	b_tb.uid,
	b_tb.ʱ���,
	COUNT ( b_tb.ʱ��� ),
	DENSE_RANK () OVER ( PARTITION BY b_tb.uid ORDER BY COUNT ( b_tb.ʱ��� ) DESC ) AS �������� 
FROM
	(
SELECT
	*,
CASE
	
	WHEN a_tb.hour_str >= '00' 
	AND a_tb.hour_str < '06' THEN
	'�賿' 
WHEN a_tb.hour_str >= '06' 
AND a_tb.hour_str < '12' THEN
'����' 
WHEN a_tb.hour_str >= '12' 
AND a_tb.hour_str < '18' THEN
'����' 
WHEN a_tb.hour_str >= '18' 
AND a_tb.hour_str < '24' THEN
'ҹ��' ELSE NULL 
END AS ʱ��� 
FROM
	(
	SELECT
		"2��data2".uid,
		"2��data2".occur_date,
		to_char( "2��data2".first_time, 'HH24' ) AS hour_str,
		DENSE_RANK () OVER ( PARTITION BY "2��data2".uid ORDER BY "2��data2".occur_date DESC ) AS rank_desc 
	FROM
		"2��data2" 
	ORDER BY
		"2��data2".uid,
		"2��data2".occur_date 
	) AS a_tb 
WHERE
	a_tb.rank_desc <= 4 
ORDER BY
	a_tb.uid,
	a_tb.occur_date 
	) AS b_tb 
GROUP BY
	b_tb.uid,
	b_tb.ʱ��� 
ORDER BY
	b_tb.uid,
	b_tb.ʱ��� 
	) AS c_tb 
WHERE
c_tb.�������� = 1;