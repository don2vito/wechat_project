SELECT
	"3��data3"."City_id",
	"3��data3"."Groupon_date",
	"3��data3"."End_time",
	LAG ( "3��data3"."End_time", 1 ) OVER ( PARTITION BY "3��data3"."City_id" ) AS last_End_time 
FROM
	"3��data3" 
ORDER BY
	"3��data3"."City_id",
	"3��data3"."Groupon_date",
	"3��data3"."Start_time";