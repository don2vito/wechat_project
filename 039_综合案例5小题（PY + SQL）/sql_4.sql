SELECT DISTINCT
	( "5题data1"."customerID" ) 
FROM
	"5题data1" 
WHERE
	"5题data1".product IN ( 'A' ) INTERSECT
SELECT DISTINCT
	( "5题data1"."customerID" ) 
FROM
	"5题data1" 
WHERE
	"5题data1".product IN ( 'B' ) INTERSECT
SELECT DISTINCT
	( "5题data1"."customerID" ) 
FROM
	"5题data1" 
WHERE
	"5题data1".product NOT IN ( 'C' );