---
layout: post
blog: true
title: "Essential point of Kafka"
date: 2014-10-25 21:21:19 +0900
comments: true
categories: ["Kafka", "Reading"]
author: Kai Sasaki
---

I list up some important point of Apache Kafka. These information can be obtained from [official documents](http://kafka.apache.org/documentation.html)

<!-- more -->

# Actors

* **Topics** are the unit in which each messages are stores. 
* **Producers** creates messages and giving them Kafka servers.
* **Consumers** uses each messages taken from each partitions.
* **Partitions**(which is already mentioned above) are something mailbox which retain all messages classified by topics.
* And each Kafka servers are called **Brokers**.

Producers write each message into all partitions which is taged its topic. For abstraction of separating server management and topic management, 
partitions are used. And replications are done by each partition. It does not seem that partition dones not replication itself. 
Messages in one partition are consumed by one particular consumer. This is fixed unless any failure is occured on brokers. 
Each message are kept a petiod of time even after consumed by consumers. The offset which decides the position of each message in partition is 
managed by consumer. So Kafka doesn't controll offset value. It is a good advantage from a view point of performance.

# Guarantees
The partition into which each message is delivered is decided by producer. These are appended to partition in the order they are sent.
Therefore consumer can also see messages in the order they are created. Because of replication, we can keep service even if N-1 server down
when we set replication number to N.

# References 

* [Data Modeling with Kafka? Topics and Partitions](http://stackoverflow.com/questions/17205561/data-modeling-with-kafka-topics-and-partitions)
* [Apache Kafka for Beginners](http://blog.cloudera.com/blog/2014/09/apache-kafka-for-beginners/)
* [Apache Kafka introduction](http://kafka.apache.org/documentation.html#introduction)
* [HortonWorks Kafka](http://jp.hortonworks.com/hadoop/kafka/)