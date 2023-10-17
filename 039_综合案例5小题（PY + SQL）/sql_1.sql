SELECT COUNT
	( DISTINCT "5��data1"."customerID" ) AS ��������,
	SUM ( "5��data1".quantity * "5��data1".price ) AS ���۽�� ,
	( SUM ( "5��data1".quantity * "5��data1".price ) / COUNT ( DISTINCT "5��data1"."orderID" ) ) AS �͵���,
	( SUM ( "5��data1".quantity ) / COUNT ( DISTINCT "5��data1"."orderID" ) ) AS �͵���,
	( COUNT ( "5��data1"."orderID" ) / COUNT ( DISTINCT "5��data1"."customerID" ) ) AS �˾�����Ƶ�� 
FROM
	"5��data1" 
WHERE
	"5��data1".order_date >= DATE'2020-01-01' 
	AND "5��data1".order_date <= DATE'2020-03-31';