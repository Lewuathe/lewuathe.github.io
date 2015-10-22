---
layout: post
title: "Hive UDAF mode"
date: 2015-10-22 17:55:22 +0900
comments: true
categories: ["Hive"]
author: Kai Sasaki
---

There are big difference between Hive UDF and UDAF. I found that when I was developing UDAF. Normal UDF usually process one row into one value. 
And Hive jobs are executed as MapReduce job (of course other can do run such as Tez or Spark). So in the case of ordinal UDF, it is only necessary to run 
mapper. However UDAF is different. 

<!-- more -->

UDAF must collect the data which are processed by mapper finally. In terms of MapReduce, this task can be done by reducer. Generally mapper and reducer
do not receive the same input. How can UDAF distinguish this type of difference?

## Mode

The initializer of UDAF can be called in each mapper and reducer. So we can distinguish the input difference by using `mode` passed at the initializer.

```java
init(GenericUDAFEvaluator.Mode m, ObjectInspector[] parameters)
          Initialize the evaluator.
```

This is passed to GenericUDAFEvaluator init method. Although I'd like to omit the detail of how to write UDAF here, we can figure out the difference of
each mode passed `init` method.

|mode| description|
|:----:|:-----|
| COMPLETE | from original data directly to full aggregation: iterate() and terminate() will be called. |
| FINAL | from partial aggregation to full aggregation: merge() and terminate() will be called. |
| PARTIAL1 | from original data to partial aggregation data: iterate() and terminatePartial() will be called. |
| PARTIAL2 | from partial aggregation data to partial aggregation data: merge() and terminatePartial() will be called. |

`iterate` is called at the input of mapper and `merge` is called at the input of reducer. So you can select by seeing this mode.
When you find `COMPLETE` or `PARTIAL1`, that means a corresponding task receives input from table records. When you find `FINAL` or `PARTIAL2`
that means a task receives mapper output. The code can be like

```java
if (m == GenericUDAFEvaluator.Mode.COMPLETE || m == GenericUDAFEvaluator.Mode.PARTIAL1) {
  // Configure for mapper input. (e.g. check argument length)
} else if (m == GenericUDAFEvaluator.Mode.FINAL || m == GenericUDAFEvaluator.Mode.PARTIAL2) {
  // Configure for reducer input.
}
```

And also you can select output type by using this mode in the same way. Thank you.




