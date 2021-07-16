WITH tb AS (SELECT "��������������"."id","��������������"."year",mode() WITHIN GROUP (ORDER BY "��������������".num)
FROM "��������������"
GROUP BY "��������������"."id","��������������"."year"
ORDER BY "��������������"."id","��������������"."year")

SELECT tb.id,
SUM((CASE WHEN tb.year='2020' THEN tb.mode ELSE NULL END)::INT) AS "2020",
SUM((CASE WHEN tb.year='2021' THEN tb.mode ELSE NULL END)::INT) AS "2021" 
FROM tb
GROUP BY
tb.id
ORDER BY tb.id