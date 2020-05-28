SELECT
	rank_data."�ı���1",
	rank_data."�ı���2",
	rank_data."�ı���3",
	rank_data."��ֵ",
	RANK () OVER ( PARTITION BY rank_data."�ı���1" ORDER BY rank_data."��ֵ" DESC ) AS International_rank,
	DENSE_RANK () OVER ( PARTITION BY rank_data."�ı���1" ORDER BY rank_data."��ֵ" DESC ) AS Chinese_rank 
FROM
	rank_data 
ORDER BY
	rank_data."�ı���3"