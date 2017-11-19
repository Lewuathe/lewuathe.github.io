---
title: "Radix Sort in Python"
layout: post
date: 2017-11-19 11:25:00 +0900
image: 'images/'
description:
tag: ["Algorithm", "Sort", "Python"]
blog: true
author: "lewuathe"
---

[Radix sort](https://en.wikipedia.org/wiki/Radix_sort) is a sorting algorithm. This algorithm is efficient if we already know the range of target values. The time complexity of the algorithm is $$O(nk)$$. $$n$$ is the size of input list and $$k$$ is the digit length of the number. For example, The digit length of 512 is 3. 

This video was a good resource to learn how radix sort works. He introduced radix sort algorithm with a plain diagram and English. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/XiuSW_mEn7g?rel=0" frameborder="0" allowfullscreen></iframe>

Radix sort depends on other sort algorithm whose time complexity is $$O(n)$$, otherwise it does not achieve $$O(nk)$$ in total. [Counting sort](https://en.wikipedia.org/wiki/Counting_sort) is used in this case. Counting sort is also efficient if we know the range of input values in advance. It's simple to implement. Counting sort just counts the occurrance of each object. Then we can know the index of each object in sorted list by using the time of occurance. 

My counting sort code is this:

```python
def counting_sort(arr, max_value, get_index):
  counts = [0] * max_value

  # Counting - O(n)
  for a in arr:s
    counts[get_index(a)] += 1
  
  # Accumulating - O(k)
  for i, c in enumerate(counts):
    if i == 0:
      continue
    else:
      counts[i] += counts[i-1]

  # Calculating start index - O(k)
  for i, c in enumerate(counts[:-1]):
    if i == 0:
      counts[i] = 0
    counts[i+1] = c

  ret = [None] * len(arr)
  # Sorting - O(n)
  for a in arr:
    index = counts[get_index(a)]
    ret[index] = a
    counts[get_index(a)] += 1
  
  return ret
```

`get_index` is used in next radix sort. The time complexity of counting sort as you know is $$O(n + k)$$. If $$k$$ is sufficiently smaller than the size of input, counting sort is very efficient. 

Of course there is no free lunch. The space complexity of counting sort is relatively high because it needs to keep the frequency of each object in the list. So counting sort is recommended to be used when the range of input values is not so high.

Radix sort uses this counting sort algorithm internally. 

1. Sort the input by counting sort per each digit from lower digit.
2. We can get a sorted list finally

That's it! This is Python code for radix sort I wrote.

```python
def get_digit(n, d):
  for i in range(d-1):
    n //= 10
  return n % 10

def get_num_difit(n):
  i = 0
  while n > 0:
    n //= 10
    i += 1
  return i

def radix_sort(arr, max_value):
  num_digits = get_num_difit(max_value)
  # O(k(n+k))
  for d in range(num_digits):
    # Counting sort takes O(n+k)
    arr = counting_sort(arr, max_value, lambda a: get_digit(a, d+1))
  return arr
```

Counting sort's computation order is $$O(n + k)$$. Radix sort needs to run counting sort $$k$$ times. In total time complexity of radix sort is $$O(k(n+k))$$.

The characteristic of radix sort to be noted here is that it is stable sorting alrogithm. It means it keeps the orinal order of same objects. For example, assuming we have a list:

```
[1, 3, 5, 6, 1', 3', 5']
```

1 and 1' are both evaluated as 1 but they are different object. A stable sort algorithm always sort this list into:

```
[1, 1', 3, 3', 5, 5', 6]
```

Non stable sorting algorithm can sort it into:

```
[1', 1, 3, 3', 5', 5, 6]
```

This feature is important especially in real world because we often want to sort a list of complex object. (e.g. User, Company, Log etc..) Even if we sort users by their age, we often want to keep the order in each group of age. Radix sort natually guarantee the stability of sort.

