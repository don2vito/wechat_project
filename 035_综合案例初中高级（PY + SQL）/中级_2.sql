SELECT AVG
	( c_table.sum_duration ) 
FROM
	(
SELECT
	b_table.city,
	a_table.ACTION,
	SUM ( CAST ( a_table.active_duration AS INTEGER ) ) AS sum_duration 
FROM
	"���и߼�data1" AS a_table
	INNER JOIN "���и߼�data2" AS b_table ON a_table.uid = b_table.uid 
WHERE
	a_table.d <= DATE'2021-01-07' - INTERVAL '1 day' 
	AND a_table.d >= DATE'2021-01-07' - INTERVAL '7 day' 
	AND b_table.city = '����' 
GROUP BY
	b_table.city,
	a_table.ACTION 
	) AS c_table;