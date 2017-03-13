---
layout: post
blog: true
title: "Import your own data with td CLI"
date: 2015-10-28 14:34:37 +0900
comments: true
categories: ["TreasureData"]
author: Kai Sasaki
---

I'm little consused to use `td` CLI to import my own data into [Treasure Data service](http://www.treasuredata.com/). In terms of bulk import, there some concept you should know.
Of course it is not difficult. Once you understand the internals, you might be able to make the import process more efficient. The detail is [here](http://docs.treasuredata.com/articles/bulk-import).

<!-- more -->

# Steps

There are some steps to do bulk import with td CLI. To begin with, I'd like to explain these steps.

## create

td import has a concept called **session**. By using this session, you can upload multiple data and do a transactional import. The required information to create session are database name and table name.

```bash
$ td import:create my_session my_db my_table
```

## prepare

The original your data often is huge. It may be troublesome and inefficient to upload these data as it is. So `prepare` aims to convert the format into [MessagePack](http://msgpack.org/index.html) and compress.
In this phase no data are transferred into TreasureData service. All tasks of `prepare` phase can be done on your local machine.

```bash
$ td import:prepare ./mylogs_20151028.csv \
     --format csv \
     -o ./output_20151028 
```

## upload

After converted, you can upload these data with `upload` subcommand into your session. 

```bash
$ td import:upload my_session ./output_20151028/*
```

The data is uploaded through secure connection into TreasureData row-based storage system.

## perform

Then the uploaded data is transformed into our column-oriented data format using MapReduce. With this process, the uploaded data is converted into more efficient format.

```bash
## In order to prevent other script from 
## uploading data into this session
$ td import:freeze
$ td import:perform my_session
```

Then your data will be stored into columnar-based storage. If you want to upload additional data with the same session, `unfreeze` command can be used. 

```bash
$ td import:unfreeze my_session
```

## commit

After you confirm the perform job is completed, you can import the data into your target table of your database. 

```bash
td import:commit my_session
```

All you want to do is finished. (No additional data to upload) You can delete your session used for this upload.

```bash
$ td import:delete my_session
```


# Last but not least
 
Although it is important to understand internal of importing process, it is a little tough work to do always. So you can do these process with one command
by using `--auto-XX` options. This is the easist way to import!

```bash
$ td import:upload \
  --auto-create my_database.my_table \
  --auto-perform \
  --auto-commit \
  --column-header \
  --output output_today \
  data_*.csv
```

