SELECT
	rank_data."文本列1",
	rank_data."文本列2",
	rank_data."文本列3",
	rank_data."数值",
	RANK () OVER ( PARTITION BY rank_data."文本列1" ORDER BY rank_data."数值" DESC ) AS International_rank,
	DENSE_RANK () OVER ( PARTITION BY rank_data."文本列1" ORDER BY rank_data."数值" DESC ) AS Chinese_rank 
FROM
	rank_data 
ORDER BY
	rank_data."文本列3"