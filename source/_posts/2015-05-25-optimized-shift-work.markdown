---
layout: post
title: "Optimized shift work"
date: 2015-05-25 17:25:29 +0900
comments: true
categories: ["python", "math"]
author: Kai Sasaki
---

Previously I received a request from my wife about optimization of shift work in restaurant where she is working. At ordinal Japanese family restaurant, the shift table is created by owner's hand.
This is very troublesome when you have to satisfy not only the members's requirements but also the sutainability of business of your restaurant. This is really tough work.
However, now is the 21th century. Computers can help us solve these type of problems. I solved this problem as an [linear programming problem](http://en.wikipedia.org/wiki/Linear_programming).

<!-- more -->

# Return shift optimization to LP problem

First we have to define the problem in the form that computers can solve. Linear programming problems requires one object function and some conditions which variables must obey.
In this case we can assume that each members submit their wish about their shift. I defined this constants as member's **satisfactions**. `S_i` represents the satisfaction of member `i`.
Each working time can have two parameters, day and time. Usually day is a day of the week because shift wishes are submitted about every week. And time can be assumed such as morning, afternoon and evening.
So totally satisfactions can be representd as `S_ijk`, i represents the index of the member `i`, `j` is the day of the week such as Monday, `k` is the working time of the day such as morning. For example if `S_123` is 0.3,
this expresses "The member of 1 when he works day 2 at time 3 satisfies him 0.3 degree."
Then it is also necessary to define variables which we want to decide the optimal combination. `x_ijk` is the binary value which represents the member `i` works or not day `j` at time `k`.
We want to decide these variables under some conditions at the same time to optimize object function. What should be optimized in this case? I defined the total satisfaction of all members.
In other words, the formula can be written as

$$
\sum_{i, j, k} S_{i,j,k} x_{i,j,k}
$$

All requirements about restaurant side should be written as conditions. In this time, in any time the number of total members who is working at restaurant must be greaer than 3.
So we can describe this condition as follow.

$$
\forall j,k \sum_{i} x_{i,j,k} >= 3 
$$

# Description of problem

I used [pulp](https://github.com/coin-or/pulp) which is python package for solving linear programming problems. This is a great framework because it retains descriptive expressions which is useful to define a lot of variables and conditions in python code. This is the description about this problem.

```python
#
#  i: arbeit_i N
#  j: day      7
#  k: time     3
#
#  S_ijk: Satisfaction of member i join at day j and k.
#  x_ijk: 1 or 0
#
#  Conditions:
#  sum x_ijk > 3
#   i
#

import numpy as np
import pulp

N = 5  # The number of members
D = 7  # The number of days in week
T = 3  # The number of time for working in a day


# Generate satisfaction matrix for each members.
# If the original, it should be passed from each member requirements.
S = np.random.rand(N, D, T) - 0.5

# Generate variables which represent each members attends or not.
var = pulp.LpVariable.dicts('VAR', (range(N), range(D), range(T)), 0, 1, 'Binary')

# Setting of object function
obj = None
for i in range(N):
    for j in range(D):
        for k in range(T):
            obj += S[i][j][k] * var[i][j][k]

problem = pulp.LpProblem('shift', pulp.LpMaximize)

problem += obj

# Setting condition 1.
# It represents a restaurant requires 3 members on each time at least.
for j in range(D):
    for k in range(T):
        c = None
        for i in range(N):
            c += var[i][j][k]
        problem += c >= 3

print problem
```

It is a nice point that we can write conditions inside `for` loop with pulp framework! I wonder the number of variables may overwhelm computing power, but it was a maginary fears.

# Solve problem

Constructing problem just has been done. We are now ready for solving problem, but only we have to do is writing some line of code.

```python
# Solve problem. Whole tasks is passes pulp framework!
status = problem.solve()

# If pulp can find optimal values which satisfies conditions, print "Optimal"
print "Status", pulp.LpStatus[status]

print "--- Result ---"
for i in range(N):
    print "Member{}".format(i)
    for j in range(D):
        print "{}day".format(j),
        for k in range(T):
            status = "NO"
            if var[i][j][k].value() > 0.0:
                status = "OK"
            print "Time{} => {},".format(k, status),
        print ""
    print ""

```

Print result.

```
Result
Member0
0day Time0 => NO, Time1 => NO, Time2 => OK,
1day Time0 => NO, Time1 => NO, Time2 => OK,
2day Time0 => OK, Time1 => OK, Time2 => NO,
3day Time0 => NO, Time1 => OK, Time2 => OK,
4day Time0 => OK, Time1 => NO, Time2 => NO,
5day Time0 => NO, Time1 => OK, Time2 => OK,
6day Time0 => NO, Time1 => NO, Time2 => NO,

Member1
0day Time0 => OK, Time1 => OK, Time2 => NO,
1day Time0 => OK, Time1 => OK, Time2 => OK,
2day Time0 => OK, Time1 => NO, Time2 => OK,
3day Time0 => OK, Time1 => OK, Time2 => NO,
4day Time0 => NO, Time1 => OK, Time2 => OK,
5day Time0 => OK, Time1 => NO, Time2 => NO,
6day Time0 => OK, Time1 => OK, Time2 => OK,

Member2
0day Time0 => NO, Time1 => OK, Time2 => OK,
1day Time0 => OK, Time1 => OK, Time2 => NO,
2day Time0 => NO, Time1 => OK, Time2 => OK,
3day Time0 => OK, Time1 => NO, Time2 => OK,
4day Time0 => OK, Time1 => NO, Time2 => NO,
5day Time0 => OK, Time1 => NO, Time2 => NO,
6day Time0 => OK, Time1 => OK, Time2 => OK,

Member3
0day Time0 => OK, Time1 => OK, Time2 => OK,
1day Time0 => NO, Time1 => OK, Time2 => NO,
2day Time0 => NO, Time1 => NO, Time2 => NO,
3day Time0 => NO, Time1 => NO, Time2 => OK,
4day Time0 => OK, Time1 => OK, Time2 => OK,
5day Time0 => OK, Time1 => OK, Time2 => OK,
6day Time0 => NO, Time1 => NO, Time2 => NO,

Member4
0day Time0 => OK, Time1 => NO, Time2 => NO,
1day Time0 => OK, Time1 => NO, Time2 => OK,
2day Time0 => OK, Time1 => OK, Time2 => OK,
3day Time0 => OK, Time1 => OK, Time2 => NO,
4day Time0 => OK, Time1 => OK, Time2 => OK,
5day Time0 => NO, Time1 => OK, Time2 => OK,
6day Time0 => OK, Time1 => OK, Time2 => OK,
```

We can see when each member will work at this restaurant.

# Ending

I couldn't expect such a easy to solve linear programming problems before trying it. (Even first I was thinking about writing code from scratch.) In this trying, the based data is generated at random.
I want to try with the real data and check the result is really good or not and the validity of the definition of problem.
Thank you.
