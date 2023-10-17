/*
CREATE AGGREGATE group_concat(anyelement)
(
sfunc = array_append, -- 每行的操作函数，将本行append到数组里 
stype = anyarray,  -- 聚集后返回数组类型 
initcond = '{}'    -- 初始化空数组
);
*/ SELECT
toy_dataset."name",
array_to_string( group_concat ( toy_dataset."text" ), '-' ) 
FROM
	toy_dataset 
GROUP BY
	toy_dataset."name" 
ORDER BY
	toy_dataset."name" ASC