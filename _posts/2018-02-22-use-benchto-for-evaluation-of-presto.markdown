---
title: "Use Benchto for evaluation of Presto"
layout: post
date: 2018-02-22 13:48:36 +0900
image: 'spools.jpg'
description:
tag: ['Benchto', 'Presto']
blog: true
author: "lewuathe"
---

Measuring performance of distributed system is not easy task. It often takes time to generate dataset, 
write queries, running them and keep the performance result. In spite of the fixed form of measuring process, 
we often have to reinvent wheels because the difference of the interface of distributed systems. Every system does not support ANSI SQL. Even [Hive](http://hive.apache.org/) and [Presto](https://prestodb.io/) do not provide compatible SQL syntax and functionality. 

[Benchto](https://github.com/prestodb/benchto) is a macro framework to define and run macro benchmark in clustered environment. It is a tool mainly developed by team of Presto in Facebook and Teradata. Although it was useful, the usage was a little complex to me. That's the reason why I tried to clarify how to use Benchto to measure Presto cluster performance. 

# Launch Benchto Service

The overview of Benchto is here. 

![overview](images/posts/2018-02-22-use-benchto-for-evaluation-of-presto/benchto-overview.png)

Mainly there are three components in Benchto required to run benchrmatk.

## benchto-service

The data store to keep the result of benchmark. It needs RDBMS like PostgreSQL to persistent the result to be reviewed later. It provides a simple web UI to compare the result by environment. It shows:

* duration
* total cpu time
* total blocked time
* output data size
* processed input data size
* total scheduled time
* total planning time
* peak memory reservation

![UI](images/posts/2018-02-22-use-benchto-for-evaluation-of-presto/benchto-ui.png)

It provides sufficient informatio to review cluster performance. Though the UI is not rich itself, it is very easy to launch the service. First you need RDBMS to store the result. benchto-service recognizes the database in local machine as default. So you can use docker container for test.

```
$ docker run --name benchto-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres
```

Now you have a PostgreSQL which can be accessed through 5432 port. benchto-service can be launched from the repository.

```
$ cd benchto
$ env SERVER_PORT=8081 ./mvnw spring-boot:run -pl benchto-service
```

You will be able to see the UI by accessing [localhost:8081](http://localhost:8081). 

## benchto-driver

benchto-driver is a Java application which loads queries to be run and test it against distributed system you want to test. That's the one to be created per distributed database system. Presto project already provides the driver for Presto. We can use the driver in order to run benchmark against your Presto cluster. Driver for Presto is installed as `presto-benchto-benchmarks` module. We need to prepare several configurations to run the benchmark. 

Profile is used for specifying the cluster uri and environment where the result is stored. The profile looks like this:

```
benchmark-service:
  url: http://localhost:8081

data-sources:
  presto:
    url: jdbc:presto://your.presto.coordinator.com:8080
    driver-class-name: com.facebook.presto.jdbc.PrestoDriver

environment:
  name: test-env

presto:
  url: http://your.presto.coordinator.com:8080

benchmark:
  feature:
    presto:
      metrics.collection.enabled: true

macros:
  sleep-4s:
    command: echo "Sleeping for 4s" && sleep 4
```

The name of file should be `application-<Profile Name>.yaml`. Please make sure the extension of the file to be `.yaml` not `.yml`. Then we need to define the benchmark spec in yaml file as well. Let's assume we saved the file with name `tpch.yaml`.


```
datasource: presto
query-names: presto/tpch/${query}.sql
runs: 3
prewarm-runs: 2
before-execution: sleep-4s
frequency: 7
database: tpch
prefix: ""
variables:
  1:
    query: q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12, q13, q14, q15
    schema: sf100
```

If you want to run benchmark with TPC-H or TPC-DS, Presto already provides the neceessary resources in `presto-benchto-benchmarks/src/main/resources/sql/presto`. `query-names` specifies the SQLs to be run. You can embed variables in this file. `database`, `schema` will be rendered in the query file so that we change the table just by editing `tpch.yaml`. 

We can launch benchto-driver with this command.

```
$ cd presto
$ ./mvnw clean package -pl presto-benchto-benchmarks
$ java \
    -jar presto-benchto-benchmarks/target/presto-benchto-benchmarks-0.196-SNAPSHOT-executable.jar \
    --sql=presto-benchto-benchmarks/src/main/resources/sql \
    --benchmarks=. \
    --activeBenchmarks=tpch \
    --profile=<Profile Name>
```

`--sql` and `--benchmarks` specify the directory for SQLs and benchmark spec files to be run respectively. `--activeBenchmarks` and `--profile` specify the benchmark spec and profile to be run. If all configuration is set properly, queries will be submitted to the cluster and you will be able to see the result stored in benchto-service. 

# Reference

* [Benchto](https://github.com/prestodb/benchto)
* [presto-benchto-benchmark](https://github.com/prestodb/presto/tree/master/presto-benchto-benchmarks)
* [TPC-H](http://www.tpc.org/tpch/)
* [TPC-DS](http://www.tpc.org/tpcds/)
