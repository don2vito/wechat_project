SELECT
	"���и߼�data1".uid,
	"���и߼�data1"."action",
	SUM (
	CAST ( "���и߼�data1".active_duration AS INTEGER )) AS sum_duration 
FROM
	"���и߼�data1" 
WHERE
	"���и߼�data1".d >= to_date( '2021-01-01', 'YYYY-MM-DD' ) 
	AND "���и߼�data1".d <= to_date( '2021-01-03', 'YYYY-MM-DD' ) 
	AND "���и߼�data1"."action" = 'jobs' 
GROUP BY
	"���и߼�data1".uid,
	"���и߼�data1"."action" 
HAVING
	SUM (
	CAST ( "���и߼�data1".active_duration AS INTEGER )) > 100;