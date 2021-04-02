SELECT
	tb.* 
FROM
	(
	SELECT
		"新3题data3"."区",
		"新3题data3"."店铺名称",
		SUM ( "新3题data3"."订单数" ) AS 订单数合计,
		DENSE_RANK ( ) OVER ( PARTITION BY "新3题data3"."区" ORDER BY SUM ( "新3题data3"."订单数" ) DESC ) AS 组内降序排序 
	FROM
		"新3题data3" 
	GROUP BY
		"新3题data3"."区",
		"新3题data3"."店铺名称" 
	) AS tb 
WHERE
	tb.组内降序排序 <= 3;