SELECT
	"初中高级data1".uid,
	"初中高级data1"."action",
	SUM (
	CAST ( "初中高级data1".active_duration AS INTEGER )) AS sum_duration 
FROM
	"初中高级data1" 
WHERE
	"初中高级data1".d >= to_date( '2021-01-01', 'YYYY-MM-DD' ) 
	AND "初中高级data1".d <= to_date( '2021-01-03', 'YYYY-MM-DD' ) 
	AND "初中高级data1"."action" = 'jobs' 
GROUP BY
	"初中高级data1".uid,
	"初中高级data1"."action" 
HAVING
	SUM (
	CAST ( "初中高级data1".active_duration AS INTEGER )) > 100;