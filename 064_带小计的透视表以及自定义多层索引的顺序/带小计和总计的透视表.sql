-- 查看数据
SELECT
	* 
FROM
	test_pivot_subtotal 
	LIMIT 5;
	
	
-- 透视
SELECT
	test_pivot_subtotal."地域",
	test_pivot_subtotal."省份",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2020 THEN test_pivot_subtotal."数量" :: INT ELSE 0 END ) AS "2020 数量",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2021 THEN test_pivot_subtotal."数量" :: INT ELSE 0 END ) AS "2021 数量",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2022 THEN test_pivot_subtotal."数量" :: INT ELSE 0 END ) AS "2022 数量",
  SUM (test_pivot_subtotal."数量" :: INT) AS "总计 数量",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2020 THEN test_pivot_subtotal."金额" :: INT ELSE 0 END ) AS "2020 金额",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2021 THEN test_pivot_subtotal."金额" :: INT ELSE 0 END ) AS "2021 金额",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2022 THEN test_pivot_subtotal."金额" :: INT ELSE 0 END ) AS "2022 金额",
	SUM (test_pivot_subtotal."金额" :: INT) AS "总计 金额",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2020 THEN test_pivot_subtotal."市值" :: INT ELSE 0 END ) AS "2020 市值",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2021 THEN test_pivot_subtotal."市值" :: INT ELSE 0 END ) AS "2021 市值",
	SUM ( CASE WHEN test_pivot_subtotal."产品年" :: INT = 2022 THEN test_pivot_subtotal."市值" :: INT ELSE 0 END ) AS "2022 市值", 
  SUM (test_pivot_subtotal."市值" :: INT) AS "总计 市值"
FROM
	test_pivot_subtotal 
GROUP BY
	ROLLUP ( test_pivot_subtotal."地域", test_pivot_subtotal."省份" ) 
ORDER BY
	test_pivot_subtotal."地域",
	test_pivot_subtotal."省份";