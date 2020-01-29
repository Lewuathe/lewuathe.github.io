---
layout: post
blog: true
title: "How to INSERT INTO with psycopg2"
date: 2016-06-04 21:36:40 +0900
comments: true
image: assets/img/posts/2016-06-04-remind-for-insert-into-with-psycopg2/catch.png
categories: ["python", "PostgreSQL"]
tag: ["Python", "PostgreSQL", "Database"]
author: Kai Sasaki
blog: true
---

The most famous library to connect PostgreSQL from Python might be [psycopg2](http://initd.org/psycopg/docs/).
psycopg2 is a simple and easy library for the people who want to manipulate SQL simply. The usage is basically pretty straightforward but I got stuck when I tried to a record into PostgreSQL via psycogpg2. Here I wrote a query like this.

```python
import psycopg2

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

But I cannot see any data in `a_table`. The query seems fine itself because we can insert into with the query. Why the data was not inserted properly?
I took some time to search for an answer and finally find a solution.

We need to call `commit` of cursor object. In short, we need to write code like below.

```python
import psycopg2

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

Since I usually use `commit` with the only transactional operation, I have thought it won't necessary to call it to simply inserting data when I don't use transaction.
So that was my bad. We should check the documentation carefully especially when we use a new library for us.
psycopg2 documentation is [here](http://initd.org/psycopg/docs/).

Thanks!

<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1449355730&asins=1449355730&linkId=821d014eded5702990704ba84efa3acc&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>
<iframe style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src="//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ac&ref=qf_sp_asin_til&ad_type=product_link&tracking_id=lewuathe-20&marketplace=amazon&region=US&placement=1491963417&asins=1491963417&linkId=2dc898cf772980fdf3d0a5dc423f3144&show_border=false&link_opens_in_new_window=true&price_color=333333&title_color=0066c0&bg_color=fafafa">
    </iframe>