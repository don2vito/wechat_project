SELECT
	"4题data1"."userID",
	SUM ( CAST ( "4题data1".monetary AS INTEGER ) ) 
FROM
	"4题data1" 
GROUP BY
	"4题data1"."userID" 
ORDER BY
	"4题data1"."userID";