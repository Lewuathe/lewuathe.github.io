---
title: "Assemble and creating table in Hive UDF"
layout: post
date: 2016-07-24 21:18:25 +0900
image: 'images/'
description:
tags: ['Hive']
blog: true
jemoji:
author: lewuathe
---

`histogram_numeric` is a UDAF which should calculate the distribution of given records. But at the same time
it should generate a table that represents one category by one row. In this point we can regard this type of
UDF is a combination of UDAF and UDTF. For example the output of `histogram_numeric` looks like

```sql
hive> SELECT explode(histogram_numeric(val, 3)) AS x FROM test_table;
```

| x | y|
| :------------- | :------------- |
| -3.62       | 10       |
| -0.12 | 3 |
| 5.24 | 12 |

So you can realize this operation by combination with `explode` function. Since `explode` separate one line array
into multiple rows, `histogram_numeric` creates one row which includes multiple records such as

```
[{"x":-3.62,"y":10},{"x":-0.12,"y":3},{"x":5.24,"y":12}]
```

There is no way to do assemble multiple records and generate multiple rows at once in one UDF. So this is a way
to do so. But I'm now searching better way. If you know, please let me know.

Thanks.
