SELECT
	"初中高级data1".d,
	COUNT ( DISTINCT "初中高级data1".uid ) 
FROM
	"初中高级data1" 
WHERE
	"初中高级data1".d >= to_date( '2021-01-01', 'YYYY-MM-DD' ) 
	AND "初中高级data1".d <= to_date( '2021-01-31', 'YYYY-MM-DD' ) 
GROUP BY
	"初中高级data1".d 
ORDER BY
	"初中高级data1".d;