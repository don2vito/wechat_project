SELECT AVG
	( CAST ( a_tb.���û������� AS INTEGER ) ) AS ���û�ƽ�������� 
FROM
	(
SELECT
	"4��data1"."userID",
	"4��data1"."date",
	"4��data2".reg_date,
CASE
	
	WHEN "4��data1"."date" = "4��data2".reg_date THEN
	"4��data1".monetary ELSE NULL 
	END AS ���û�������,
CASE
		
		WHEN "4��data1"."date" <> "4��data2".reg_date THEN
		"4��data1".monetary ELSE NULL 
	END AS ���û������� 
FROM
	"4��data1"
	LEFT JOIN "4��data2" ON "4��data1"."userID" = "4��data2"."userID" 
) AS a_tb;