SELECT AVG
	( CAST ( a_tb.老用户购买金额 AS INTEGER ) ) AS 老用户平均购买金额 
FROM
	(
SELECT
	"4题data1"."userID",
	"4题data1"."date",
	"4题data2".reg_date,
CASE
	
	WHEN "4题data1"."date" = "4题data2".reg_date THEN
	"4题data1".monetary ELSE NULL 
	END AS 新用户购买金额,
CASE
		
		WHEN "4题data1"."date" <> "4题data2".reg_date THEN
		"4题data1".monetary ELSE NULL 
	END AS 老用户购买金额 
FROM
	"4题data1"
	LEFT JOIN "4题data2" ON "4题data1"."userID" = "4题data2"."userID" 
) AS a_tb;