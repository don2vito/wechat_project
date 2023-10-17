SELECT
	"2题data1"."serveID",
	MAX ( "2题data1".maximum ) AS maximum,
	( MAX ( "2题data1".maximum ) - MAX ( "2题data1".maximum ) * 0.001 ) AS minus_1_1000 
FROM
	"2题data1" 
WHERE
	to_date( to_char( "2题data1".occur_time, 'yyyy-mm-dd' ), 'yyyy-mm-dd' ) >= DATE'2021-02-13' - INTERVAL '7 day' 
	AND to_date( to_char( "2题data1".occur_time, 'yyyy-mm-dd' ), 'yyyy-mm-dd' ) <= DATE'2021-02-13' - INTERVAL '1 day' 
	AND "2题data1".metric_name LIKE'%Cpu%' 
GROUP BY
	"2题data1"."serveID";