SELECT
	"���и߼�data1".d,
	COUNT ( DISTINCT "���и߼�data1".uid ) 
FROM
	"���и߼�data1" 
WHERE
	"���и߼�data1".d >= to_date( '2021-01-01', 'YYYY-MM-DD' ) 
	AND "���и߼�data1".d <= to_date( '2021-01-31', 'YYYY-MM-DD' ) 
GROUP BY
	"���и߼�data1".d 
ORDER BY
	"���и߼�data1".d;