SELECT
	"4��data1"."userID",
	SUM ( CAST ( "4��data1".monetary AS INTEGER ) ) 
FROM
	"4��data1" 
GROUP BY
	"4��data1"."userID" 
ORDER BY
	"4��data1"."userID";