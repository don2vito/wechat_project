SELECT C
	."userID",
	C.�������� 
FROM
	(
SELECT
	b."userID",
	to_number( b."date" :: TEXT, '9999999999999' ) - b.rk1 AS ����ʱ��,
	COUNT ( to_number( b."date" :: TEXT, '9999999999999' ) - b.rk1 ) AS �������� 
FROM
	(
SELECT A
	.*,
	ROW_NUMBER () OVER ( PARTITION BY A."userID" ORDER BY A."date" ASC ) AS rk1 
FROM
	( SELECT DISTINCT "4��data1"."userID", "4��data1"."date" FROM "4��data1" ) AS A 
	) AS b 
GROUP BY
	b."userID",
	to_number( b."date" :: TEXT, '9999999999999' ) - b.rk1 
	) AS C 
WHERE
	C.�������� = 3;