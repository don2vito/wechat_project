SELECT
	"3题data1"."Order_id（主键）" 
FROM
	"3题data1"
	INNER JOIN (
SELECT
	"3题data1"."User_id",
	SUM ( CAST ( "3题data1"."Amount" AS INTEGER ) ) 
FROM
	"3题data1" 
GROUP BY
	"3题data1"."User_id" 
HAVING
	SUM ( CAST ( "3题data1"."Amount" AS INTEGER ) ) > 50 
	) AS a_table ON "3题data1"."User_id" = a_table."User_id";