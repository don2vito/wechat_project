SELECT
	b_table.career_level,
	a_table.ACTION,
	SUM ( CAST ( a_table.active_duration AS INTEGER ) ) AS sum_duration 
FROM
	"初中高级data1" AS a_table
	INNER JOIN "初中高级data2" AS b_table ON a_table.uid = b_table.uid 
WHERE
	a_table.d = DATE'2021-01-03' - INTERVAL '1 day' 
GROUP BY
	b_table.career_level,
	a_table.ACTION;
	
SELECT SUM
	( CAST ( "初中高级data1".active_duration AS INTEGER ) ) 
FROM
	"初中高级data1" 
WHERE
	"初中高级data1".d = DATE'2021-01-03' - INTERVAL '1 day';
	
SELECT
  c_table.sum_duration * 100 / ( SELECT SUM ( CAST ( "初中高级data1".active_duration AS INTEGER )) FROM "初中高级data1" WHERE "初中高级data1".d = DATE'2021-01-03' - INTERVAL '1 day' ) AS pct 
FROM
	(
SELECT
	b_table.career_level,
	a_table.ACTION,
	SUM ( CAST ( a_table.active_duration AS INTEGER ) ) AS sum_duration 
FROM
	"初中高级data1" AS a_table
	INNER JOIN "初中高级data2" AS b_table ON a_table.uid = b_table.uid 
WHERE
	a_table.d = DATE'2021-01-03' - INTERVAL '1 day' 
GROUP BY
	b_table.career_level,
	a_table.ACTION 
	) AS c_table;
	
SELECT AVG(d_table.pct)
FROM 
(SELECT
  c_table.sum_duration * 100 / ( SELECT SUM ( CAST ( "初中高级data1".active_duration AS INTEGER )) FROM "初中高级data1" WHERE "初中高级data1".d = DATE'2021-01-03' - INTERVAL '1 day' ) AS pct 
FROM
	(
SELECT
	b_table.career_level,
	a_table.ACTION,
	SUM ( CAST ( a_table.active_duration AS INTEGER ) ) AS sum_duration 
FROM
	"初中高级data1" AS a_table
	INNER JOIN "初中高级data2" AS b_table ON a_table.uid = b_table.uid 
WHERE
	a_table.d = DATE'2021-01-03' - INTERVAL '1 day' 
GROUP BY
	b_table.career_level,
	a_table.ACTION 
	) AS c_table) AS d_table;