---
layout: post
title: "Agile Samurai Basecamp in Tokyo <2>"
date: 2013-12-09 20:16
comments: true
categories: ["Agile", "Samurai", "TDD"]
author: Kai Sasaki
---

This entry follows previous post.
The practical methods about TDD are explained in this section.

And also, it is written as an article of [TDD advent calendar on 10th day](http://qiita.com/advent-calendar/2013/tddadventjp).

## How to start TDD? Takuto Wada(twada)

The left wing of agile is what about team environment, management, scrum, iteration and standup meeting. On the other hand, the right wing of agile is not perceived enough to ordinary people.
It's CI/CD and automation. These are also as important as the formers. There is apparent difference between making software and keeping making software. Agile programming always requires refactoring.
In TDD process, refactoring is the core process. You cannot say that you achieve TDD without refactoring your program. 

### Write running code, and then write clean code

Making Good design previously is difficult task. Besides we don't know what is good design on the system undefined yet. Software and program are too complex for us to understand perfectly.
So we cannot avoid progressing development with positivism notion. In other words, write code first! However we cannot solve all problems yet. The codes once confirmed as what runs with no bugs
are not willing to be refactored. We are afraid of changing running code. TDD enables us to pass over these fears. The concrete cycle of TDD is below.

### TDD cycle

1. Make TODO list
2. Write test code first
3. Running test and fail (*Red phase*)
4. Write product code
5. Running test and success (*Green phase*)
6. Refactoring product code with keeping Green
7. Repeat 1~6 process

The most important process in these 7 phases is refactoring. If you result in failure of TDD, the main reason is to neglect refactoring your product code. It needs more power of the will.
So it is better to insert refactoring into TDD process. You don't do refactoring as an addition, but do as necessary process.

![Golden Cycle](/images/posts/2013-12-10-samurai-2/golden_cycle.jpg)

### The secrets of TDD

To achive TDD, you should know how to start TDD at your daily work.

### *Small start one by one*

You should make small TODO list as possible. It is good to reduce each task within the span which you can complete red, green and refactoring cycle in 15~30minutes. 
The more fast you can complete, the better your TODO list is. 

### *Tackle one enemy in one time*

However, if you can reduce each task in small unit, starting all tasks at one time is not good work. As Samurai(Musashi Miyamoto) did, you have to also complete tasks one by one.
You can concentrate the essentials of each task, 

### *You are the first user*

When you write test code, you should take care of the usability. The interface of your product code is determined when you write your test code. 
So before write your test code and while writing your test code, your should try and make the interface better bacause you are the first user of your product.
The only way to know how user friendly your product is using it yourself. In other words, let's test it.

### *Test your uncertain*

The purpose of TDD is not mainly to guarantee software quality, but to take your ease in order to sleep peacefully. If there are no automatic test codes, it is horror.
The every time you release your products, you are to end up with praying for the success of the release. Or in order to assure that there are no bugs in your software, 
you might have to many overtime work. That's too bad :(. To avoid this situation, test codes are selected and written under the criteria of how this test makes you peaceful.

### *Knit a lifeline*

This is relevant to previous item. Compiled a lot of test codes will help you when you are in danger or crisis. This test codes become a lifeline knitted over many layers
It will support you in any situation strongly.

### *The essencial goal of TDD*

The best goal of TDD is keeping your health. This means your code health, your team health and of course your code health. Bacause of TDD, all developers can go home early,
take a meal with your family and friends, make your product with peaceful mind. This is the essential goal of TDD for all software engineers. Conquering your anxiety and keeping you healthy.

# After session

This goal made me realize why I am a software engineer again. Programming, writing code should always be fun. It should always be what makes me happy.
If you are unhappy with writing code as work, it mistakes the means for the end, doesn't it? TDD is the one way of making my life as software engineer more joyful.
That mind must not be forgot whenever I type my test code.

The each line of your test codes makes you happy, I believe.





