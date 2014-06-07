---
layout: post
title: "Marble problem"
date: 2014-03-18 21:45:14 +0900
comments: true
categories: ["AtCoder", "memolization"]
author: Kai Sasaki
---

I tried this problem.

## Marble

There are boxes infinitely in a straight line. Each box is labeled from left side ...,-2,-1,0,1,2,... to the right side.
Now *R* red marbles are in the -100th box. In the same way, *G* green mables are in the 0th box and *B* blue mables are in the 100th box.
There no other marbles in all boxes. All boxes should have one marble at most.
Repeat below process and make the number of marbles of each each at most one.

* Select one marble, move it left box or right box.
* However one box must not have more than two marbles that has different colors each other

Calculate minimum required steps.

<!-- more -->

I wrote below code.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Created by sasakiumi on 3/18/14.
 */
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int r = sc.nextInt();
        int g = sc.nextInt();
        int b = sc.nextInt();
    
        int max = Math.max(Math.max(r, g), b);
    
        List<Integer> steps = new ArrayList<Integer>();
        steps.add(0);
        for (int i = 1; i <= max; i++) {
            Integer pre = steps.get(i - 1);
            steps.add(pre + (i / 2));
        }
    
        Integer ans = steps.get(r) + steps.get(g) + steps.get(b);
        System.out.println(ans);
    }
}
```

OK. I understand this code does not put the case of 100 marbles that is same color into consideration.
If there are 200 red marbles, this code does not work properly. But I have not found effective way to solve all cases.
I will update this problem later. If you have any good idea, please let me know.

Thank you.
