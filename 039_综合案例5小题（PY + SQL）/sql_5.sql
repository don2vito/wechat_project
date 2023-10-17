SELECT
	a_tb."city",
	a_tb."customerID",
	a_tb.购买金额 
FROM
	(
SELECT
	"5题data3"."city",
	"5题data1"."customerID",
	SUM ( "5题data1"."price" * "5题data1"."quantity" ) AS 购买金额,
	DENSE_RANK () OVER ( PARTITION BY "5题data3".city ORDER BY SUM ( "5题data1".price * "5题data1".quantity ) DESC ) AS 组内降序排名 
FROM
	"5题data1"
	RIGHT JOIN "5题data3" ON "5题data1".store = "5题data3".store 
WHERE
	"5题data1"."quantity" IS NOT NULL 
GROUP BY
	"5题data3"."city",
	"5题data1"."customerID" 
	) AS a_tb 
WHERE
	a_tb.组内降序排名 = 2;