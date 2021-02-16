SELECT
	view_group_n_days."﻿uid",
	MAX ( MAX ) 
FROM
	view_group_n_days 
GROUP BY
	view_group_n_days."﻿uid" 
ORDER BY
	view_group_n_days."﻿uid";