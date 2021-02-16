CREATE VIEW "view_distinct_n_days" AS  SELECT DISTINCT n_days."﻿uid",
    n_days.login_time
   FROM n_days;
ALTER TABLE "view_distinct_n_days" OWNER TO "postgres";

CREATE VIEW "view_group_n_days" AS  SELECT view_minus_n_days."﻿uid",
    view_minus_n_days.minus,
    max(view_minus_n_days.rank) AS max
   FROM view_minus_n_days
  GROUP BY view_minus_n_days."﻿uid", view_minus_n_days.minus;
ALTER TABLE "view_group_n_days" OWNER TO "postgres";

CREATE VIEW "view_minus_n_days" AS  SELECT view_rank_n_days."﻿uid",
    view_rank_n_days.login_time,
    view_rank_n_days.rank,
    ((view_rank_n_days.login_time)::date - (view_rank_n_days.rank)::integer) AS minus
   FROM view_rank_n_days;
ALTER TABLE "view_minus_n_days" OWNER TO "postgres";

CREATE VIEW "view_rank_n_days" AS  SELECT view_distinct_n_days."﻿uid",
    view_distinct_n_days.login_time,
    dense_rank() OVER (PARTITION BY view_distinct_n_days."﻿uid" ORDER BY view_distinct_n_days.login_time) AS rank
   FROM view_distinct_n_days;
ALTER TABLE "view_rank_n_days" OWNER TO "postgres";

