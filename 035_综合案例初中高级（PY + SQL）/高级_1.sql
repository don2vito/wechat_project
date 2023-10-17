SELECT C
	.uid,
	C.连续天数 
FROM
	(
SELECT
	b.uid,
	to_number( b.d :: TEXT, '9999999999999' ) - b.rk1 AS 连续时间,
	COUNT ( to_number( b.d :: TEXT, '9999999999999' ) - b.rk1 ) AS 连续天数 
FROM
	(
SELECT A
	.*,
	ROW_NUMBER () OVER ( PARTITION BY uid ORDER BY d ASC ) AS rk1 
FROM
	( SELECT DISTINCT uid, d FROM "初中高级data1" ) AS A 
	) AS b 
GROUP BY
	b.uid,
	to_number( b.d :: TEXT, '9999999999999' ) - b.rk1 
	) AS C 
WHERE
	C.连续天数 = 2;