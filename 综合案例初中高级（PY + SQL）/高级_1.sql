SELECT C
	.uid,
	C.�������� 
FROM
	(
SELECT
	b.uid,
	to_number( b.d :: TEXT, '9999999999999' ) - b.rk1 AS ����ʱ��,
	COUNT ( to_number( b.d :: TEXT, '9999999999999' ) - b.rk1 ) AS �������� 
FROM
	(
SELECT A
	.*,
	ROW_NUMBER () OVER ( PARTITION BY uid ORDER BY d ASC ) AS rk1 
FROM
	( SELECT DISTINCT uid, d FROM "���и߼�data1" ) AS A 
	) AS b 
GROUP BY
	b.uid,
	to_number( b.d :: TEXT, '9999999999999' ) - b.rk1 
	) AS C 
WHERE
	C.�������� = 2;