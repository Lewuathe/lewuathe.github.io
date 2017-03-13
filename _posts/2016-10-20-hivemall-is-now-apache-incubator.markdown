---
title: "Hivemall is now Apache Incubator!"
layout: post
date: 2016-10-20 20:26:10 +0900
image: 'images/'
description:
tag: ['Hive', 'Hivemall', 'Apache']
blog: true
author: 'lewuathe'
---

![Hivemall Logo](/images/hivemall_bg.png)

Today I have a big news. Now Hivemall joined Apache incubator project! Hivemall is a scalable machine learning library running on Hadoop.
It was originally developed by [Yui Makoto](https://github.com/myui/) who is a research engineer at [Treasure Data Inc](http://www.treasuredata.com/).

So from now, we call it [Apache Hivemall](http://hivemall.incubator.apache.org/). [Top page](http://hivemall.incubator.apache.org) is now opened.
Apache Hivemall is developed as Hive UDF. Therefore we can integrated Apache Hivemall with Spark or other projects which has compatibility to Hive UDF easily. There are two ways for getting started.

* Add jar and defined function in your Hive cluster
* Use [Treasure Data](https://www.treasuredata.com/)

## Install by yourself

If you have already Hive cluster, your can easily install Apache Hivemall as ordinal Hive UDF.

```
$ hive
> add jar /path/to/hivemall-core-xxx-with-dependencies.jar;
> source /path/to/define-all.hive;
```

These resource can be downloaded from [here](https://github.com/myui/hivemall/releases). `hivemall-core`  is core module which includes various type of
UDFs. `hivemall-nlp` includes natural language processing utilities with its own dictionary. `hivemall-spark` is for Spark integration as you can see.

## Use Treasure Data

Apache Hivemall is hosted by Treasure Data service. So if you don't want to have your own Hive cluster and maintain it, that's a good option.
Apache Hivemall is just a collection of Hive UDF. So data analysts or engineers who use SQL in their daily analysis can easily start using Apache Hivemall.

![hivemall_version](/images/hivemall_version.png)

Though Apache Hivemall has just started incubation project, there are a lot of ideas to be developed. Please check [Hivemall JIRA](https://issues.apache.org/jira/browse/HIVEMALL/?selectedTab=com.atlassian.jira.jira-projects-plugin:summary-panel) and [issues on GitHub](https://github.com/myui/hivemall/issues).
In addition, we are now preparing guideline and roadmap for incubation releases. Please keep eye on them.

Last but not least, it is very important to make community broad and wider for incubation project. Apache Hivemall very welcomes patches anytime.
So please join our community as developer, user and any other type of contributor.

Thanks!
