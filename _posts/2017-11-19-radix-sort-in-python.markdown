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

[Radix sort](https://en.wikipedia.org/wiki/Radix_sort) is a sorting algorithm. This algorithm is efficient if we already know the range of target values. The time complexity of the algorithm is $$O(nk)$$. $$n$$ is the size of the input list and $$k$$ is the digit length of the number. For example, The digit length of 512 is 3. 

This video was a good resource to learn how radix sort works. He introduced the radix sort algorithm with a plain diagram and English. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/XiuSW_mEn7g?rel=0" frameborder="0" allowfullscreen></iframe>

Radix sort depends on another sort algorithm whose time complexity is $$O(n)$$, otherwise, it does not achieve $$O(nk)$$ in total. [Counting sort](https://en.wikipedia.org/wiki/Counting_sort) is used in this case. Counting sort is also efficient if we know the range of input values in advance. It's simple to implement. Counting sort just counts the occurrence of each object. Then we can know the index of each object in a sorted list by using the time of occurrence. 

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

`get_index` is used in the next radix sort. The time complexity of counting sort as you know is $$O(n + k)$$. If $$k$$ is sufficiently smaller than the size of the input, counting sort is very efficient. 

Of course, there is no free lunch. The space complexity of counting sort is relatively high because it needs to keep the frequency of each object in the list. So counting sort is recommended to be used when the range of input values is not so high.

Radix sort uses this counting sort algorithm internally. 

1. Sort the input by counting sort per each digit from the lower digit.
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

The characteristic of radix sort to be noted here is that it is a stable sorting algorithm. It means it keeps the original order of the same objects. For example, assuming we have a list:

```
[1, 3, 5, 6, 1', 3', 5']
```

1 and 1' are both evaluated as 1 but they are a different object. A stable sort algorithm always sorts this list into:

```
[1, 1', 3, 3', 5, 5', 6]
```

Non stable sorting algorithm can sort it into:

```
[1', 1, 3, 3', 5', 5, 6]
```

This feature is important especially in the real world because we often want to sort a list of complex object. (e.g. User, Company, Log etc..) Even if we sort users by their age, we often want to keep the order in each group of age. Radix sort naturally guarantees the stability of a sort.

Sort algorithms are the basic algorithms to learn the CS class. If you want to learn the data structures and algorithms, [**Introduction to Algorithms, 3rd Edition**](https://amzn.to/2N3HZ1M) is the best book I've ever read.

<div style='text-align: center'>
<a href="https://www.amazon.com/Introduction-Algorithms-3rd-MIT-Press/dp/0262033844/ref=as_li_ss_il?ie=UTF8&qid=1549979958&sr=8-2&keywords=data+structure&linkCode=li3&tag=lewuathe-20&linkId=be365cf59c624c4668f8446f23add2f4" target="_blank"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=0262033844&Format=_SL250_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=lewuathe-20" ></a><img src="https://ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=li3&o=1&a=0262033844" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</div>

I don't think it's an exaggeration to say it's a bible to learn the algorithm and data structure and algorithms. It may be an overkill for just learning the sort algorithms but I believe it brings you a bunch of insight and fundamental pieces of knowledge about the algorithm and data structures every CS students should learn.
