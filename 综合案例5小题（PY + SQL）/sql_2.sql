SELECT
	concat_ws (
	'',
	CAST ((
SELECT COUNT
	( DISTINCT a_tb."customerID" ) 
FROM
	(
SELECT
	"5��data1"."customerID",
	"5��data1"."orderID",
	COUNT ( "5��data1"."orderID" ) AS count_orderid 
FROM
	"5��data1" 
WHERE
	"5��data1".order_date >= DATE'2019-05-01' 
	AND "5��data1".order_date <= DATE'2020-04-30' 
GROUP BY
	"5��data1"."customerID",
	"5��data1"."orderID" 
HAVING
	COUNT ( "5��data1"."orderID" ) >= 2 
	) AS a_tb 
	) * 100 / (
SELECT COUNT
	( DISTINCT b_tb."customerID" ) 
FROM
	(
SELECT
	"5��data1"."customerID",
	"5��data1"."orderID",
	COUNT ( "5��data1"."orderID" ) AS count_orderid 
FROM
	"5��data1" 
WHERE
	"5��data1".order_date >= DATE'2019-05-01' 
	AND "5��data1".order_date <= DATE'2020-04-30' 
GROUP BY
	"5��data1"."customerID",
	"5��data1"."orderID" 
	) AS b_tb 
	) AS TEXT 
	),
	'%' 
	);