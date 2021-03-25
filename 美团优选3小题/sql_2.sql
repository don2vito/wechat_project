SELECT COUNT
	( CASE WHEN d_table.gmv >= 0 AND d_table.gmv < 500 THEN d_table.province_name ELSE NULL END ) AS gmv_0_500,
	COUNT ( CASE WHEN d_table.gmv >= 500 AND d_table.gmv < 1000 THEN d_table.province_name ELSE NULL END ) AS gmv_500_1000,
	COUNT ( CASE WHEN d_table.gmv >= 1000 THEN d_table.province_name ELSE NULL END ) AS gmv_1000_ 
FROM
	(
SELECT
	c_table.province_name,
	SUM (
	CAST ( c_table.gmv AS INTEGER )) AS gmv 
FROM
	(
SELECT
	a_table.city_num,
	a_table.gmv,
	b_table.province_name 
FROM
	"美团data1" AS a_table
	INNER JOIN "美团data2" AS b_table ON a_table.city_num = b_table.city_num 
	) AS c_table 
GROUP BY
	c_table.province_name 
	) AS d_table;