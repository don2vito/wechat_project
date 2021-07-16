WITH tb AS (SELECT "多条件计算众数"."id","多条件计算众数"."year",mode() WITHIN GROUP (ORDER BY "多条件计算众数".num)
FROM "多条件计算众数"
GROUP BY "多条件计算众数"."id","多条件计算众数"."year"
ORDER BY "多条件计算众数"."id","多条件计算众数"."year")

SELECT tb.id,
SUM((CASE WHEN tb.year='2020' THEN tb.mode ELSE NULL END)::INT) AS "2020",
SUM((CASE WHEN tb.year='2021' THEN tb.mode ELSE NULL END)::INT) AS "2021" 
FROM tb
GROUP BY
tb.id
ORDER BY tb.id