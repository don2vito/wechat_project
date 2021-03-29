SELECT C
	."userID",
	C.连续天数 
FROM
	(
SELECT
	b."userID",
	to_number( b."date" :: TEXT, '9999999999999' ) - b.rk1 AS 连续时间,
	COUNT ( to_number( b."date" :: TEXT, '9999999999999' ) - b.rk1 ) AS 连续天数 
FROM
	(
SELECT A
	.*,
	ROW_NUMBER () OVER ( PARTITION BY A."userID" ORDER BY A."date" ASC ) AS rk1 
FROM
	( SELECT DISTINCT "4题data1"."userID", "4题data1"."date" FROM "4题data1" ) AS A 
	) AS b 
GROUP BY
	b."userID",
	to_number( b."date" :: TEXT, '9999999999999' ) - b.rk1 
	) AS C 
WHERE
	C.连续天数 = 3;