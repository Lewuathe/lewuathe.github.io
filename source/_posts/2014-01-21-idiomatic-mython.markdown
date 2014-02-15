---
layout: post
title: "Idiomatic Python ~I will write with this style~"
date: 2014-01-21 13:18
comments: true
categories: ["Python", "Idiomatic"]
author: Kai Sasaki
---

I read a book, *[Writing Idiomatic Python](http://www.amazon.co.jp/Writing-Idiomatic-Python-2-7-3-Knupp-ebook/dp/B00B5KG0F8)*
Although I usually write python codes, I have not paid attension to the style of these codes. By reading this book, I have noticed
that there are pythonic style in python codes. And I think it was good mind to write python code. There were many *Halmful*, *Idiomaric*
phrases about python code. So I'd like to introduce some of them which I'll write in my own code.

<!-- more -->

And of course, all python developers should read this book!!

## Enumerate

Usually, I write loop code like below.

```python
index = 0
for element in ["Takeshi", "Nobita", "Masao"]:
    print('{}:{}'.format(index, element))
    index += 1
```

But it is harmful according to this book. Correctly, you should write like below.

```python
conteiner = ["Takeshi", "Nobita", "Masao"]
for index, element in enumerate(conteiner):
    print('{}:{}'.format(index, element)
```


## Arbitrary arguments

In python, you can write arbitrary arguments with `*args` or `**kwargs`. Arbutrary arguments are useful when you 
want to implement some types of API which is different by package versions. You can write like below.

```python
def make_api_call(a, b, c, *args, **kwargs):
    print a
	print b
	print c
	print args
	print kwargs
```

Run this

```python
#!/usr/bin/python

if __name__ == "__main__":
    make_api_call(1, 2, 3, 4, 5, 6, name="Takeshi", age=23)

# --console--
# 1
# 2
# 3
# (4, 5, 6)
# {'age': 23, 'name': 'Takeshi'}
#

```

## Avoid *Swallowing* useful exceptions

In python, `exception` is common phrases used in `for` loop or etc. In addition to this,
`exception` gives you a useful information for debugging. So you should not *swallow* these exceptions
by writing bare `except` clause. If you don't have any idea about what type exceptions are raised from 
third-party library, you should raise it again.

```python
import requests
def get_json_response(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        raise
```

## Avoid using a temporary variables with swapping

Use tuple.

```python
foo = "FOO"
bar = "BAR"
(foo, bar) = (bar, foo)
```

## Use `join` method. It's more faster

```python
result_list = ["Takeshi", "Nobita", "Masuo"]
reesult_string = " ".join(result_list)
```

## Use format function to make a formatted string

```python
# user is a dictionary
def get_formatted_user_info(user):
    output = 'Nama: {user.name}, Age: {user.age}, Sex: {user.sex}'.format(user=user)
```

## Prefer `xrange` to `range`

Use `xrange`

```python
for index in xrange(10000):
    print('index: {}'.format(index)
```

## Default value got from dicionary

If there are `name` field in user, `get` returns `'Unknown'`.

```python
username = user.get('name', 'Unknown')
```

## Dictionary complehension

The list complehension is well known about python context. But dictionary complehension is as important as this.


```python
user_email = {user.name: user.email for user in users_list if user.email}
```

## Set complehension

In set syntax, you can use complehension expression.

```python
users_first_names = {user.first_name for user in users}
```

## Ignore unnecessary row in tuple

If there are any data which is not necessary for you in tuple, ignore it with `_`

```python
(name, age, _, _) = get_user_info(user)
if age > 20:
    output = '{name} can drink!'.format(name=name)
```

## Generator

Python list comprehension is very useful, however, processing very large list will run out of memory.
In this case you should use `generator` which is iterative expression, but doesn't use memory.

```python
users = ["Nobita", "Takeshi", "Masuo"]
for i in (user.upper() for user in users if user != "Takeshi"):
    print(i)

# NOBITA
# MASUO
```

## Refer PEP8

Python has standard set of formatting rule officially. It is called **PEP8**.
You should install this plugin your editor.

## Write as PEP252

PEP257 is the set of rules of document formattings.

```python
def calculate_statistics(value_list):
    """Return a tuple containing the mean, median and the mode of a list of integers

    Arguments:
    value_list -- a list of integer values

    """
```


# Last but not least

I am a pythonia. With reading this book, I am able to write more pythonic code at my work scene.

