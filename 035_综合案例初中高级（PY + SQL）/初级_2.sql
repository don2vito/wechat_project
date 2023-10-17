SELECT
	a_table.d,
	a_table.ACTION 
FROM
	(
SELECT
	"���и߼�data1".d,
	"���и߼�data1"."action",
	MAX ( "���и߼�data1".active_duration ) AS max_duration,
	DENSE_RANK () OVER ( PARTITION BY "���и߼�data1".d ORDER BY MAX ( "���и߼�data1".active_duration ) DESC ) AS rank_duration 
FROM
	"���и߼�data1" 
WHERE
	"���и߼�data1".d >= to_date( '2021-01-01', 'YYYY-MM-DD' ) 
	AND "���и߼�data1".d <= to_date( '2021-01-31', 'YYYY-MM-DD' ) 
GROUP BY
	"���и߼�data1".d,
	"���и߼�data1"."action" 
ORDER BY
	"���и߼�data1".d,
	MAX ( "���и߼�data1".active_duration ) DESC 
	) AS a_table 
WHERE
	a_table.rank_duration = 1;