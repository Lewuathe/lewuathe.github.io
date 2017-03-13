---
layout: post
blog: true
title: "Closure with Async.js"
date: 2013-12-05 20:29
comments: true
categories: ["Node", "JavaScript", "async"]
author: Kai Sasaki
---

You may use [Async.js](https://npmjs.org/package/async) at least one time when you develop with nodejs.

> Async is a utility module which provides straight-forward, powerful functions for working with asynchronous JavaScript.

So if you want to write asynchronous code with JavaScript, I recommend you to use it. It's easy to use, simple syntax.
However I had trouble with using Async.js in the context of giving dynamic task array. In this article, I want to share 
how to write dynamic task array given to Async.js module.

## Problem

I wrote like a below code with nodejs.

```js
var async = require('async');

// Total task is 10 which is executed in parallel
var TASK_NUM = 10;

// All task functions are put in taskList
var taskList = [];
for (var i = 0; i < TASK_NUM; i++) {
    taskList.push(function(callback) {
        console.log(i);
        callback(null, i);
    });
}

async.parallel(taskList, function(err, results) {
    console.log(results);
});
```

When you run this code, I obtained below output.

```
10
10
10
10
10
10
10
10
10
10
[ 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 ]
```

This didn't fit my expectation. I thought all tasks should get i-th argument. So each task's output
is i-th number, if i-th task runs. However in this case, all task's output is 10. Why closure in function(In JavaScript, `function` makes variable scope, called closure) might not be effective?

## Answer

There is answer in [StackOverflow](http://stackoverflow.com/questions/12472448/async-parallel-with-functions-dynamic-array).

> A closure doesn't "trap" the value that an outer variable had at the time it was created; it "traps" a reference to whatever value the outer variable has at the time it's executed (which in this case won't be until well after your for loop has finished.

So in this case, closure does not make scope when it is **declared**, but **executed**. The variable `i` resulted in 10 after `for` loop in this code. And then each tasks will be executed under the condition that variable `i` is 10. I understood why these odd phenomenon was occured.

## How to write

How should I write in order to execute this code as I expected in advance. Same page showed me the answer.

```
var deleteFunction = makeDeleteFunction(i, callback);
```

Writing wrapper function which wraps my original tasks makes scope under given argument `i`. When you declare task, you should not make task function directly, but should give parameters which trapped in declaration context to the wrapper function. Here is my sample that is corresponds to above code.

```js
var async = require('async');

// Wrapper function
function makeTask(i) {
    return function(callback) {
        console.log(i);
        callback(null, i);
    };
}

// Total task is 10 which is executed in parallel
var TASK_NUM = 10;

// All task functions are put in taskList
var taskList = [];
for (var i = 0; i < TASK_NUM; i++) {
    taskList.push(makeTask(i));
}

async.parallel(taskList, function(err, results) {
    console.log(results);
});
```

Then output is given as I expected.

```
0
1
2
3
4
5
6
7
8
9
[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
```

If you write dynamic task function with Async.js, notice these fact.

