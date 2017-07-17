---
title: "DB Migration with Flyway"
layout: post
date: 2017-07-14 21:19:57 +0900
image: 'images/'
description:
tag: ["Flyway", "Database", "Scala"]
blog: true
author: "lewuathe"
---

Now database migration should be managed under version control system. Every database schema can be changed through time.
If we don't track this, it must be difficult to rollback or test. We often use [ActiveRecord](http://guides.rubyonrails.org/active_record_basics.html) as migration script because it is database agnostic and easy to write.

But Ruby script is not the best choice when we are developing Java/Scala libraries. I looked for the tool that can be easily integrated with [Maven](http://maven.apache.org/) or [SBT](http://www.scala-sbt.org/). [Flyway](https://flywaydb.org/getstarted/) looked the best to me.

![flyway logo](images/posts/2017-07-14-db-migration-with-flyway/flyway-logo-tm.png)

Flyway is a database migration tool which can be easily integrated various kind of build systems. Flyway adapted a simple [architecture](https://flywaydb.org/getstarted/how).

At the first time Flyway runs, it creates the table which manages the version of each database schema. It called **metadata table**. Since this is the important table for Flyway, please don't be amazed at the unknown table in your database. Flyway first sort each DDLs according to their version. And then it applied to tables while checking applied schemas in metadata table. The detail is described [here](https://flywaydb.org/getstarted/how).

Since I used Flyway as SBT plugin, I'll explain about the usage briefly.

First you need to write down dependency on that plugin. It can be written in `project/plugins.sbt`

```
addSbtPlugin("org.flywaydb" % "flyway-sbt" % "4.2.0")

resolvers += "Flyway" at "https://flywaydb.org/repo"
```

Schema are written as DDL in some SQL files. We need to specify the location where these SQL files are stored.

```
flywayLocations := Seq("filesystem:core/src/main/resources/db/migration"),

// Necessary for initializing metadata table
flywayBaselineOnMigrate := true,
```

Then you can write your schema under `core/src/main/resources/db/migration`. For example, `V1__Create_person.sql` can be like this.

```
create table PERSON (
    ID int not null,
    NAME varchar(100) not null
);
```

The name convention looks `<Version>__<Verb>_<Table Name>.sql`. Of course we don't need to obey but it's recommended so that other Flyway user can understand.

Finally migration can be run through sbt command.

```
$ ./sbt -Dflyway.url=$JDBC_URL \
    -Dflyway.user=$USERNAME \
    -Dflyway.password=$PASSWORD \
    flywayMigrate
```

Flyway converges the database schema according to given DDLs. It can be run through `sbt` command. So you can easily
integrate Flyway SBT with Jenkins or other CI tools.

Thanks

## Reference

- [Active Record](http://guides.rubyonrails.org/active_record_basics.html)
- [Flyway SBT](https://flywaydb.org/getstarted/firststeps/sbt)
- [SBt](http://www.scala-sbt.org/)
