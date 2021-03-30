SELECT
	a_tb."city",
	a_tb."customerID",
	a_tb.������ 
FROM
	(
SELECT
	"5��data3"."city",
	"5��data1"."customerID",
	SUM ( "5��data1"."price" * "5��data1"."quantity" ) AS ������,
	DENSE_RANK () OVER ( PARTITION BY "5��data3".city ORDER BY SUM ( "5��data1".price * "5��data1".quantity ) DESC ) AS ���ڽ������� 
FROM
	"5��data1"
	RIGHT JOIN "5��data3" ON "5��data1".store = "5��data3".store 
WHERE
	"5��data1"."quantity" IS NOT NULL 
GROUP BY
	"5��data3"."city",
	"5��data1"."customerID" 
	) AS a_tb 
WHERE
	a_tb.���ڽ������� = 2;