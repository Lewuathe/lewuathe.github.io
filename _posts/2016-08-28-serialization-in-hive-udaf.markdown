---
title: "Serialization in Hive UDAF"
layout: post
date: 2016-08-28 20:39:36 +0900
image: 'images/'
description:
tag: ["Hive", "Java"]
blog: true
jemoji:
author: "lewuathe"
---

Serialization of Java sometimes complex and difficult to understand for me. I've read [Effective Java](https://www.amazon.com/Effective-Java-2nd-Joshua-Bloch/dp/0321356683) and
javadoc of JDK SE api docs. So I knew I understood the basic concept of serialization of Java object. But I have faced to a problem when I wrote Hive UDAF.
This might be a problem every people encountered when they try to write Hive UDAF. So I try to list up the problem and the fact I found this time.

<!-- more -->

# Hive SerDe requires hadoop.io.Text

You cannot use primitive Java object like `String` as output of UDAF. The output of UDAF is passed by `terminate` method of `GenericUDAFEvaluator`.
But you cannot use `int`, `String` and other primitive Java objects here because Hive SerDe does not recognize it.
You should use `IntWritable`, `DoubleWritable` and `Text` object provided by Hadoop MapReduce framework.

# Unserializable hadoop.io.Text

In Hive UDAF, we should pass aggregated data from mapper to reducer. Otherwise we cannot obtain correct result of aggregated data.
It can be done with `terminatePartial` and `merge` method of `GenericUDAFEvaluator`.

```java
@Override
public Object terminatePartial(AggregationBuffer aggregationBuffer)
    throws HiveException {
  MyBuffer buf = (MyBuffer)aggregationBuffer;
  return buf.serialize();
}
```

You can make any class which inherits `AggregationBuffer` of Hive. Since `terminatePartial` returns any `Object`, it is better to serialize explicitly.
You should implement serialize method to do so. But I found one thing here. `MyBuffer` includes [`hadoop.io.Text`](https://hadoop.apache.org/docs/r2.6.2/api/org/apache/hadoop/io/Text.html)
class because output should be `Text` object. But this code throws exception because `Text` is not serializable.

I found we must convert String (or other serializable object) to Text object in `terminate` object because AggregationBuffer cannot contain `Text` object
unless `buf.serialize()` returns actually serializable object. In our case `terminate` method looks linkedin

```java
List<String> stringList = // String list returned by AggregationBuffer
Object[] row = new Object[n]; // row is returned object which represents one row.
for (int i = 0; i < n; i++) {
  row[i] = new Text(stringList.get(i));
}
return row;
```

In summary,

- We cannot use `hadoop.io.Text` in `AggregationBuffer` in UDAF because it is not serializable.
- We should return `hadoop.io.Text` as returned object from UDAF otherwise Hive SerDe cannot recognize it.
