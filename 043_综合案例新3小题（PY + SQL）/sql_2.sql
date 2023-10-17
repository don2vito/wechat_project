SELECT
	"新3题data2"."姓名",
	SUM ( CASE WHEN "新3题data2"."科目" = '语文' THEN "新3题data2"."分数" ELSE NULL END ) AS 语文,
	SUM ( CASE WHEN "新3题data2"."科目" = '数学' THEN "新3题data2"."分数" ELSE NULL END ) AS 数学,
	SUM ( CASE WHEN "新3题data2"."科目" = '外语' THEN "新3题data2"."分数" ELSE NULL END ) AS 外语,
	SUM ( "新3题data2"."分数" ) AS 总分,
	ROUND( AVG ( "新3题data2"."分数" ), 2 ) AS 平均分 
FROM
	"新3题data2" 
GROUP BY
	"新3题data2"."姓名";