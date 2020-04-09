---
title: "Light way to remove whitespace in PostgreSQL"
layout: post
date: 2020-04-09 21:13:03 +0900
image: 'assets/img/posts/2020-04-09-remove-whitespace-in-postgresql/catch.jpg'
description:
tag: ['PostgreSQL', 'SQL']
blog: true
author: "Kai Sasaki"
---

We might have the experience to remove the white space in the string recorded in PostgreSQL. There is a function [`TRIM`](https://www.postgresqltutorial.com/postgresql-trim-function/), but it only removes the white space on the left/right side of the string. How can we do that when we want to omit the whitespace in the middle of the given string?

[`REGEXP_REPLACE`](https://www.postgresql.org/docs/9.4/functions-string.html) is available to replace any string with the regular expression pattern.

```sql
SELECT regexp_replace(some_string, '[\s+]', '', 'g') FROM table;
```

By using the flag `g`, it replaces all characters appearing in the given string. That would be a flexible and powerful way to replace any characters with PostgreSQL.


Photo by [Markus Spiske on Unsplash](https://unsplash.com/photos/xekxE_VR0Ec)