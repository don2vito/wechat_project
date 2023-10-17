SELECT
	b_table.city_num,
	b_table.gmv,
	SUM ( b_table.gmv ) OVER ( ORDER BY b_table.gmv,b_table.city_num) AS cumsum_gmv 
FROM
	(
SELECT
	a_table.city_num,
	SUM (
	CAST ( a_table.gmv AS INTEGER )) AS gmv 
FROM
	"√¿Õ≈data1" AS a_table 
GROUP BY
	a_table.city_num 
	) AS b_table 
ORDER BY
	b_table.gmv;