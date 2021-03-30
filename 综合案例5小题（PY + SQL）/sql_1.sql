SELECT COUNT
	( DISTINCT "5题data1"."customerID" ) AS 购买人数,
	SUM ( "5题data1".quantity * "5题data1".price ) AS 销售金额 ,
	( SUM ( "5题data1".quantity * "5题data1".price ) / COUNT ( DISTINCT "5题data1"."orderID" ) ) AS 客单价,
	( SUM ( "5题data1".quantity ) / COUNT ( DISTINCT "5题data1"."orderID" ) ) AS 客单件,
	( COUNT ( "5题data1"."orderID" ) / COUNT ( DISTINCT "5题data1"."customerID" ) ) AS 人均购买频次 
FROM
	"5题data1" 
WHERE
	"5题data1".order_date >= DATE'2020-01-01' 
	AND "5题data1".order_date <= DATE'2020-03-31';