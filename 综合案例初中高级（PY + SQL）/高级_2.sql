SELECT
	b_table.career_level,
	COUNT (a_table.uid ) 
FROM
	"���и߼�data1" AS a_table
	INNER JOIN "���и߼�data2" AS b_table ON a_table.uid = b_table.uid 
WHERE
	a_table.d >= to_date('2021-01-01', 'YYYY-MM-DD') 
	AND a_table.d <= to_date('2021-01-31', 'YYYY-MM-DD') 
GROUP BY
	b_table.career_level;