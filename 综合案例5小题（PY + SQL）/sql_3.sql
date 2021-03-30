SELECT
	"5题data3".store,
	"5题data3".city,
	"5题data3".region 
FROM
	"5题data1"
	RIGHT JOIN "5题data3" ON "5题data1".store = "5题data3".store 
WHERE
	"5题data1".quantity IS NULL;