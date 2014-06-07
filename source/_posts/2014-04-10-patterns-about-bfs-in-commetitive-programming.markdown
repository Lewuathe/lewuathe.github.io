---
layout: post
title: "Patterns about BFS in competitive programming"
date: 2014-04-10 20:24:26 +0900
comments: true
categories: ["Competitive Programming", "TopCoder", "BFS"]
author: Kai Sasaki
---

So let's go back to English from today :)

I solved SRM612 Div1 for practice. This problem is [this](http://community.topcoder.com/stat?c=problem_statement&pm=10543)
In this post, I left out the detail of this problem because main topic of this post is pattern of [BFS](http://en.wikipedia.org/wiki/Breadth-first_search).
First I tried to solve this problem with some dynamic programming algorithm. But after trying, I found BFS is sufficient algorithm
to solve. So now I rewrote my program as below.

<!-- more -->

```java
import java.util.*;
import java.math.*;

import static java.lang.Math.*;

public class EmoticonsDiv1 {
    public static int[] decode(int code) {
        int[] ret = new int[2];
        ret[0] = code / 10000;
        ret[1] = code % 10000;
        return ret;
    }

    public int printSmiles(int smiles) {
        Queue<Integer> q = new LinkedList<Integer>();
        int[][] state = new int[1 << 1000][1 << 1000];
        for (int i = 0; i < 1 << 1000; i++) {
            for (int j = 0; j < 1 << 1000; j++) {
                state[i][j] = (1 << 1000);
            }
        }

//        state[i][j] : i = message, j = clipboard
        state[1][0] = 0;
        q.add(1 * 10000 + 0);

        while (!q.isEmpty()) {
            int[] ret = decode(q.poll());
            int message = ret[0];
            int clipboard = ret[1];

            if (state[message][message] > state[message][clipboard] + 1) {
                state[message][message] = state[message][clipboard] + 1;
                q.add(message * 10000 + message);
            }

            if (message + clipboard < (1 << 1000) && state[message + clipboard][clipboard] > state[message][clipboard] + 1) {
                state[message + clipboard][clipboard] = state[message][clipboard] + 1;
                if (message + clipboard == smiles) return state[message + clipboard][clipboard];
                q.add((message + clipboard) * 10000 + clipboard);
            }

            if (message > 0 && state[message - 1][clipboard] > state[message][clipboard] + 1) {
                state[message - 1][clipboard] = state[message][clipboard] + 1;
                if (message - 1 == smiles) return state[message - 1][clipboard];
                q.add((message - 1) * 10000 + clipboard);
            }

        }

        return 1 << 1000;
    }
}


```


The computing complexity of this code is O(S^2). Could solve in time. After writing, I realized there are some patterns about writing BFS
in competitive programming. I want to put together these patterns in this port for the future contest.

## State encoding, decoding

In general, BFS uses a queue data strucure. The elements of queue has to keep each state to search. In this case, each `message` and `clipboard`.
When you write software on long-term basis, you should write state class for keeping `message` and `clipboard`. But this is competitive programming.
Defining adhoc class will take you some more time to complete writing code. So you should avoid this pattern as possible.

The solution is encoding, decoding pattern. Default queue can only keep one `Integer` or `String`, therefore let two variables put into this one variable.
Specifically, this is.

```java
// Decode one integer to two interger that composes state
public static int[] decode(int code) {
    int[] ret = new int[2];
    ret[0] = code / 10000;
    ret[1] = code % 10000;
    return ret;
}

int[] ret = decode(q.poll());
int message = ret[0];
int clipboard = ret[1];
// Encode two variables into one variable
q.add(message * 10000 + clipboard);

```

With this pattern you don't have to write your own state class. But this pattern has a fault. If there are more variables in a state,
decoding and encoding code becomes more complex and hard to debug. In addition to this problem, you should also know the range of input variable.
In this case, I use 10000 number to encoding and decoding, bacause input variables are included in [0, 1000]. So `message` and `clipboard` can be
separated. The selection of this base integer will be difficult as the number of state varibales are increasing.

## Optimization value

Above case, optimization value to be submit as answer is the count of manipulation `state[i][j]`. If you can write state class, you don't need to
this 2 dimension array. But you couldn't. So with this `state`, I can realize that if I want to keep more values such as optimization value,
I can prepair external third variable instead. With this variable, you can keep more values corresponding to each state.

## Last but not least

You should not write such codes in production software!!

