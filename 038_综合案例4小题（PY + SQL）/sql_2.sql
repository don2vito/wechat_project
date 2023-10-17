SELECT
	b_table.category,
	b_table."orderID" 
FROM
	(
SELECT
	a_table.category,
	a_table."orderID",
	DENSE_RANK () OVER ( PARTITION BY a_table.category ORDER BY a_table."sum_monetary" DESC ) AS dense_rank_desc 
FROM
	(
SELECT
	"4题data1".category,
	"4题data1"."orderID",
	SUM ( CAST ( "4题data1".monetary AS INTEGER ) ) AS sum_monetary 
FROM
	"4题data1" 
GROUP BY
	"4题data1".category,
	"4题data1"."orderID" 
	) AS a_table 
	) AS b_table 
WHERE
	b_table."dense_rank_desc" = 1;