SELECT
	concat_ws (
	'',
	CAST ((
SELECT COUNT
	( DISTINCT a_tb."customerID" ) 
FROM
	(
SELECT
	"5题data1"."customerID",
	"5题data1"."orderID",
	COUNT ( "5题data1"."orderID" ) AS count_orderid 
FROM
	"5题data1" 
WHERE
	"5题data1".order_date >= DATE'2019-05-01' 
	AND "5题data1".order_date <= DATE'2020-04-30' 
GROUP BY
	"5题data1"."customerID",
	"5题data1"."orderID" 
HAVING
	COUNT ( "5题data1"."orderID" ) >= 2 
	) AS a_tb 
	) * 100 / (
SELECT COUNT
	( DISTINCT b_tb."customerID" ) 
FROM
	(
SELECT
	"5题data1"."customerID",
	"5题data1"."orderID",
	COUNT ( "5题data1"."orderID" ) AS count_orderid 
FROM
	"5题data1" 
WHERE
	"5题data1".order_date >= DATE'2019-05-01' 
	AND "5题data1".order_date <= DATE'2020-04-30' 
GROUP BY
	"5题data1"."customerID",
	"5题data1"."orderID" 
	) AS b_tb 
	) AS TEXT 
	),
	'%' 
	);