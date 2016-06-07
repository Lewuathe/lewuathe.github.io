---
title: "Conditional mysqldump"
layout: post
date: 2016-06-07 18:34:15 +0900
image: 'images/'
description:
tags: ["MySQL", 'mysqldump']
blog: true
jemoji:
---

`mysqldump` is a useful tool for migration of database. This tool enables us to move a data
into another database through human readable format, SQL. But as default `mysqldump` dumps all records in all tables in database. I wanted to use `mysqldump` as a tool to move only specified record to another table. We can assume a situation when a data in production environment to development envinment or vice versa. So how can we achieve this with `mysqldump`.

<!-- more -->

I found a several options of `mysqldump` to do that. You can type command like below when you want to dump all.

```
$ mysqldump <database name> > dump.sql
```

I'll introduce some way to restrict dump records with given conditions.

## Dump specified table

If you want to dump only specified table records, you can do this.

```
$ mysql <database name> <table name> > dump.sql
```

`dump.sql` includes all records in a table specified as <table name>.

## Dump records specified by `WHERE` clause

If you want to restrict dumped records with given conditions like you use in `WHERE` clause, you can do this.

```
$ mysqldump <database name> <table name> --where="id like '12345'" > dump.sql
```

So `dump.sql` only includes a record whose id is '12345'. One thing to note here is you can not use '=' in `--where` option, I don't know the reason.
So if you want to match column value exactly, it's better to use `like`.

## Not to create table every time.

When you move records one by one with above queries, you might not want to recreate table every time because records inserted before are also deleted.
Although this is default behaviour of `mysqldump` there is an option not to `DROP TABLE` and recreate table every time.

```
$ mysqldump <database name> <table name> --where="id like '12345'" --no-create-info
```

By using `--no-create-info`, you can omit `DROP TABLE` and `CREATE TABLE` queries in your dump file.

After all, you can move records one by one with `mysqldump`. What make me happy in this time is `mysqldump` can also dump binary type column correctly.
This is biggest reason why I tried to use `mysqldump` to move records one by one. So if you want to move a record including binary type value such as `blob`, let's try it.

Thank you.
