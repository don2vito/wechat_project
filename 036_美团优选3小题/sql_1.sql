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
HAVING
	SUM (
	CAST ( c_table.gmv AS INTEGER )) > 500;