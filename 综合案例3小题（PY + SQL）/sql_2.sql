SELECT
	"3题data2_2"."Order_id（主键）",
	"3题data2_1"."Groupon_date" 
FROM
	"3题data2_1"
	INNER JOIN "3题data2_2" ON "3题data2_2"."Group_id" = "3题data2_1"."Group_id（主键）" 
ORDER BY
	"3题data2_2"."Order_id（主键）";