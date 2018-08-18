---
title: "Concurrent Object on Shared Memory"
layout: post
date: 2018-03-10 21:31:30 +0900
image: 'forest.jpg'
description:
tag: ['Java', 'Memory', 'Multiprocessor', 'Programming']
blog: true
author: "lewuathe"
---

I've just read Chapter 3 of [The Art of Multiprocesor Programming](https://www.amazon.com/Art-Multiprocessor-Programming-Revised-Reprint/dp/0123973376). It illustrates the detail and examples of consistency model of concurrent objects. Although it was a little complex, that topic was very interesting to me. I'm going to introduce the consistency of objects on shared memory in order to review my understanding to these consistency model.

# Concurrent Object

I'm going to explain three types of consistency model by using a example.
This example data structure is a simple [FIFO](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)).

```java
class MyQueue<T> {
  int head, tail;
  T[] items;
  public MyQueue(int capacity) {
    head = 0;
    tail = 0;
    items = (T[]) new Object[capacity]
  }
  public void enqueue(T x) throws FullException {
    if (tail - head == items.length) {
      throw new FullException();
    }
    items[tail % items.length] = x;
    tail++;
  }

  public T dequeue() throws EmptyException {
    if (tail == head) {
      throw new EmptyException();
    }
    T x = items[head % items.length];
    head++;
    return x;
  }
}
```

It's a simple FIFO. You don't need to inspect the implementation detail of the class. Just interface is used for comparaing three models. As you can see, this implementation is not thread-safe. You should not use this code in your production environment.

**Consistency Model** is a contract between our programmer and objects about the expected behaviour when the object is manipulated by multipel threads. In above example, `MyQueue` will fall into invalid state by enqueue/dequeue from multiple threads. What behaviour can we expect to this object? 

# Quiescent Consistency

Shared object is manipulated through method call which starts from *invocation* and ends at *response* event. That means method call takes some time to complete its own operation. But we can consider actual data change can happen at the point of time in the timeline. The first principal we can assume in this model is:

> Principle1: Method calls should appear to happen in a one-at-at-time sequential order. 

This principal assumes actual operation can happen at the point in the timeline. This picture illustrates the situation.

![one-at-a-time](images/posts/2018-03-10-concurrent-object-on-shared-memory/one-at-a-time.png)

Dots on the timeline in `MyQueue` object should be in specific order to make the state consistent. In quiescent consistency, we need to assume another principal. 

> Principle2: Method calls separated by a pediod of quiescence should appear to take effect in their real-time order. 

We can make sure some operations after the period cannot be overlapped the ones before the period. In this illustration, we know that operation after quiescent period never overlap with the operations before quiescent period. But operations in either side can be reordered in any order. 

![quiescent-period](images/posts/2018-03-10-concurrent-object-on-shared-memory/quiescent-period.png)

So basically quiescent consistency is a type of consistency to make sure no more change won't happen after some period of quiescence. 

Another thing to be noted here is that quiescent consistency *compositional*. A property *P* is composisitional if all subcomponent of a component satisfies the property *P*, the component should also satisfies the property *P* as a whole. Hence, when you create a component combining subcomponents which are quiescent consistent should be also quiescent consistent. 

# Sequential Consistency

In my opinion, sequential consistency is less complicated than quiescent consistency because the definition is straightforward. In order to achieve sequential consistency, a object must satisfy this principle in addition to principle1.

> Principle3: Method calls should appear to take effect in program order

*Program order* means the natual order when you run the program in single thread. For example, this execution order of method calls is not sequential consistent because the order from the viewpoing of thread A is not program order. If thread A `enqueue(x)` before `dequeue(y)`, the order of real execution on shared object should be kept same. 

![sequential-inconsistent](images/posts/2018-03-10-concurrent-object-on-shared-memory/sequential-inconsistent.png)

Also what we need to mention is that sequential consistency is not compositional. Even if you create a component integrating some sequential consistent components, it won't be sequential consistent. 

# Linearlizability

This is the strongest consistency model but it is totally easy to understand it. This consistency model must be the one you natually expect to shared objects. Protecting the data by lock or synchronization mechanism makes you data linearizable. The principle to be added to define linearlizability is here:

> Principle4: Each method call should appear to take effect instantaneously at some moment between its invocation and response. 

That indicates that a point when the data manipulation happens (*linearizable point*) should be within from *invocation* to *response*. 

![linearizable](images/posts/2018-03-10-concurrent-object-on-shared-memory/linearizable.png)

In this picture, the linearizable points of each method call shoule be within opacity squares respectively. That must match our intuition when we create shared objects so easy to understand. 

Although Java memory model does not guarantee linearizability itself, it provides some building blocks to achieve the property easily. Locks and `synchronized` blocks protects data by mutual exclution. Mutual exclution natually achieve linearlizability because critical path is just linearizable point. And also `volatile` fields are also linearizable. The update by one thread will be shown to another thread immediately. `volatile` in this case has same effect with locks and `synchronized`. But when we do multiple reads/writes that are not atomic, that's not the case. Only `volatile` does not guarantee the consistency of all variables.

Basically we need to take care of linearlizability in daily programming in most cases because it can be achieved natually by using lock mechanism. But I realized that there are many more consistency model. I would like to deep dive into them when I get a chance. Thanks.

# Reference

* [The Art of Multiprocessor Programming](https://www.amazon.com/Art-Multiprocessor-Programming-Revised-Reprint/dp/0123973376)
* [Eventual Consistencyまでの一貫性図解大全](https://qiita.com/kumagi/items/3867862c6be65328f89c)
