SELECT
	"5��data3".store,
	"5��data3".city,
	"5��data3".region 
FROM
	"5��data1"
	RIGHT JOIN "5��data3" ON "5��data1".store = "5��data3".store 
WHERE
	"5��data1".quantity IS NULL;