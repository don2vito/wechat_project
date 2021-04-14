SELECT
	date_part('week', "新3题data1"."日期"::DATE) AS 周次, 
	SUM ( "新3题data1"."订单" ) AS 订单总和,
	ROUND( SUM ( "新3题data1"."订单" ) / COUNT ( DISTINCT "新3题data1"."日期" ), 2 ) AS 日均订单,
	MAX ( "新3题data1"."订单" ) AS 极大值订单,
	MIN ( "新3题data1"."订单" ) AS 极小值订单 
FROM
	"新3题data1" 

GROUP BY
	date_part('week', "新3题data1"."日期"::DATE)
ORDER BY
	date_part('week', "新3题data1"."日期"::DATE);
