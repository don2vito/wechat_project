SELECT DISTINCT
	( "5��data1"."customerID" ) 
FROM
	"5��data1" 
WHERE
	"5��data1".product IN ( 'A' ) INTERSECT
SELECT DISTINCT
	( "5��data1"."customerID" ) 
FROM
	"5��data1" 
WHERE
	"5��data1".product IN ( 'B' ) INTERSECT
SELECT DISTINCT
	( "5��data1"."customerID" ) 
FROM
	"5��data1" 
WHERE
	"5��data1".product NOT IN ( 'C' );