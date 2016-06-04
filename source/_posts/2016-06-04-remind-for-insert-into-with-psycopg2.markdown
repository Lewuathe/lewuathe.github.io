---
layout: post
title: "Remind for INSERT INTO with psycopg2"
date: 2016-06-04 21:36:40 +0900
comments: true
categories: ["python", "PostgreSQL"]
author: Kai Sasaki
---

The most famous library to connect PostgreSQL from Python might be [psycopg2](http://initd.org/psycopg/docs/).
psycopg2 is a simple and easy to use library for who want to manipulate SQL simply. When I want to put a record into
a table, I wrote a query like this.


```python
conn = psycopg2.connect(host=pg_credential.hostname,
                        port=pg_credential.port,
                        user=pg_credential.username,
                        password=pg_credential.password,
                        database=pg_credential.path[1:]) # To remove slash

cursor = conn.cursor()
cursor.execute("INSERT INTO a_table (c1, c2, c3) VALUES(%s, %s, %s)", (v1, v2, v3))
cursor.close()
conn.close()
```

<!-- more -->

But I cannot see any data in `a_table`. The query seems fine itself because we can insert into with the query.
I took some time to search an answer and finally find a solution.

We need to call `commit` of cursor object. In short, we need to write code like below.

```python
conn = psycopg2.connect(host=pg_credential.hostname,
                        port=pg_credential.port,
                        user=pg_credential.username,
                        password=pg_credential.password,
                        database=pg_credential.path[1:]) # To remove slash

cursor = conn.cursor()
cursor.execute("INSERT INTO a_table (c1, c2, c3) VALUES(%s, %s, %s)", (v1, v2, v3))
conn.commit() # <- We MUST commit to reflect the inserted data
cursor.close()
conn.close()
```

Since I usually use `commit` with only transactional operation, I have thought it won't necessary to call it to simply inserting data.
So that was my bad. We should check the documentation carefully especially when we use a new library for us.
psycopg2 documentation is [here](http://initd.org/psycopg/docs/).

Thanks!
