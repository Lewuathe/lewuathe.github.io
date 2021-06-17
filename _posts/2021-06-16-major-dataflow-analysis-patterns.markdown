---
title: "Major Dataflow Analysis Patterns"
layout: post
date: 2021-06-16 14:30:42 +0900
image: 'assets/img/posts/2021-06-16-major-dataflow-analysis-patterns/catch.jpg'
description:
tag: ['Algorithm', 'CS']
blog: true
author: "Kai Sasaki"
---

Dataflow analysis is a technique to collect information about the possible state that can be taken at each point of flow of the program. This analysis lets us know, for instance, which variables are alive at the specific point of the program or how many times a variable is used in the program.
A [control flow graph (CFG)](https://en.wikipedia.org/wiki/Control-flow_graph) provides us the basis for this type of analysis. We can do majority type of data flow analysis on this data structure by iteratively walking through the basic blocks in the graph. For example, we have a following C/C++ program.

```c
int x = 5;
int y = 1;
while (x != 1) {
  y = x * y;
  x -= 1;
}
```

We can abstractly represent this program by using the CFG as follows.

![CFG](assets/img/posts/2021-06-16-major-dataflow-analysis-patterns/cfg.png)

Each blue block represents a code line and basic blocks are the group of blue blocks until it reaches the end of the program or branch condition.

We can accomplish following four type of data flow analysis by using this CFG.

* Reaching Definitions
* Available Expressions
* Live Variables
* Very Busy Expressions

Let's take a look how reaching definition goes as an example.

# Reaching Definitions


