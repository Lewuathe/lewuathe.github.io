---
title: "Completed 'Parallel Programming' at Cousera"
layout: post
date: 2017-05-13 22:19:10 +0900
image: 'images/'
description:
tag: ["Scala", "Parallel Programming"]
blog: true
author: "lewuathe"
---

Last week I completed ["Parallel Programming" course at Cousera](https://www.coursera.org/learn/parprog1). Since it was just before the vacation, I was a little busy to complete assignments. I'm relieved that I can finish the course.

![completed](images/posts/2017-05-13-completed-'parallel-programming'-at-cousera/completed.png)

The reason why I started the course was I wanted to improve my Scala programming skill and understanding about the parallel programming notions in Scala. Relatively known topics for me was talked in week1 and week2. But in week3 and 4, data structure for parallel programming was interesting to me. Scala provides the parallel collection data structure. We can use this data structure just by calling `par` method.

```
scala> Array(1,2,3,4,5)
res0: Array[Int] = Array(1, 2, 3, 4, 5)

scala> Array(1,2,3,4,5).par
res1: scala.collection.parallel.mutable.ParArray[Int] = ParArray(1, 2, 3, 4, 5)
```

If you run transform and other type of operation on the data structure, Scala automatically allocate parallel operations to multiple threads. So you don't need to know the detail of task assignments to each threads, CPUs.

# Commutativity and Associativity

The most important point I learned was **associativity** in parallel programming. Associativity is a characteristic of a mathematical function which can be represented as below.

\begin{equation}
f(x, f(y, z)) = f(f(x, y), z)
\end{equation}

If a function have associativity, you can run the function in parallel in the most cases because it does not require the order of running time. Another feature described in the lecture was **commutativity**.

\begin{equation}
f(x, y) = f(y, x)
\end{equation}

One thing to be taken care was that commutativity does not lead associativity. It means there are functions which satisfies commutativity but not associativity. So it is necessary to check both commutativity and associativity. By checking this before run, you can obtain consistent result of these function with parallel map or reduce operations.

Assignment were also interesting. In week3, we implemented parallel K-means algorithm. I had an experience to write K-means algorithm in sequence version but not in Scala. So that was a good resource for me to understand and compare the difference between sequential one and parallel one.

There seems to be other [Scala courses](https://www.coursera.org/specializations/scala). I also took [a functional programming Scala course](https://www.coursera.org/learn/progfun1) before. So I will be happy if i get a chance to enroll other courses to improve my Scala skill.
