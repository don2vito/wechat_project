SELECT
	"3��data1"."Order_id��������" 
FROM
	"3��data1"
	INNER JOIN (
SELECT
	"3��data1"."User_id",
	SUM ( CAST ( "3��data1"."Amount" AS INTEGER ) ) 
FROM
	"3��data1" 
GROUP BY
	"3��data1"."User_id" 
HAVING
	SUM ( CAST ( "3��data1"."Amount" AS INTEGER ) ) > 50 
	) AS a_table ON "3��data1"."User_id" = a_table."User_id";