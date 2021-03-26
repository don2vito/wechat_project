SELECT
	a_table.d,
	a_table.ACTION 
FROM
	(
SELECT
	"初中高级data1".d,
	"初中高级data1"."action",
	MAX ( "初中高级data1".active_duration ) AS max_duration,
	DENSE_RANK () OVER ( PARTITION BY "初中高级data1".d ORDER BY MAX ( "初中高级data1".active_duration ) DESC ) AS rank_duration 
FROM
	"初中高级data1" 
WHERE
	"初中高级data1".d >= to_date( '2021-01-01', 'YYYY-MM-DD' ) 
	AND "初中高级data1".d <= to_date( '2021-01-31', 'YYYY-MM-DD' ) 
GROUP BY
	"初中高级data1".d,
	"初中高级data1"."action" 
ORDER BY
	"初中高级data1".d,
	MAX ( "初中高级data1".active_duration ) DESC 
	) AS a_table 
WHERE
	a_table.rank_duration = 1;