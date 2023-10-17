SELECT
	"3题data3"."City_id",
	"3题data3"."Groupon_date",
	"3题data3"."End_time",
	LAG ( "3题data3"."End_time", 1 ) OVER ( PARTITION BY "3题data3"."City_id" ) AS last_End_time 
FROM
	"3题data3" 
ORDER BY
	"3题data3"."City_id",
	"3题data3"."Groupon_date",
	"3题data3"."Start_time";