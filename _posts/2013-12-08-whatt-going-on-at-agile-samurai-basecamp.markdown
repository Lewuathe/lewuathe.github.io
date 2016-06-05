---
layout: post
blog: true
title: "Agile Samurai Basecamp in Tokyo <1>"
date: 2013-12-08 19:29
comments: true
categories: ["Agile", "Basecaml", TDD"]
author: Kai Sasaki
---

At work, I am a scrum padawan, not yet master :-) 

Through developing with agile team, I was taught what scrum is, product backlog is, sprint is.

In order to accelerate this growth as an agile programmer, I took part in TDD section of [Agile Samurai Basecamp](http://www.agilesamuraibasecamp.org/).
TDD(Test Driven Development) is the most interesting method in my mind. So I wanted to know how to progress TDD in my daily work.
This article includes TDD core process which I study in basecamp and what I thought for the future career as a programmer.

## Keynote : Shintarou Kakutani

He is the translator of *[The Agile Samurai](http://pragprog.com/book/jtrap/the-agile-samurai)* . 
He answered the questions  who is agile samurai, what agile teams are for.

### Who is agile samurai?

![samurai](/images/posts/2013-12-08-samurai-1/samurai.jpg)

Agile team must keep to delivering valuable software every week. It doesn't mean just delivering lecture or lesson, 
but codes which run as what you and your customer expects. To achieve this, it is very important to tackle problems as *"whole one team"*  which includes
your customers. Customers decide what you make, then your decide how you make. Delivering values to customer and tackling problems as whole one team is the 
core concept of *[The Agile Samurai](http://pragprog.com/book/jtrap/the-agile-samurai)* . 

### Why did you write more Agile book?

There were already many agile books in stores. Why another agile book is needed at that time? 
In the past, there were no books which compiled main below 7 books which explains agile practice for detail.

* [Extream programming explained](http://www.amazon.co.jp/XP%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%A0%E3%83%BB%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E5%85%A5%E9%96%80%E2%80%95%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E9%96%8B%E7%99%BA%E3%81%AE%E7%A9%B6%E6%A5%B5%E3%81%AE%E6%89%8B%E6%B3%95-%E3%82%B1%E3%83%B3%E3%83%88-%E3%83%99%E3%83%83%E3%82%AF/dp/489471275X)
* [Refactoring](http://www.amazon.co.jp/Refactoring-Improving-Existing-Addison-Wesley-Technology/dp/0201485672/ref=sr_1_1?s=english-books&ie=UTF8&qid=1386502275&sr=1-1&keywords=refactoring)
* [Extream programming planning](http://www.amazon.co.jp/XP%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%A0%E3%83%BB%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E5%AE%9F%E8%A1%8C%E8%A8%88%E7%94%BB-The-Series-%E3%82%B1%E3%83%B3%E3%83%88-%E3%83%99%E3%83%83%E3%82%AF/dp/4894713411/ref=sr_1_cc_1?s=aps&ie=UTF8&qid=1386502308&sr=1-1-catcorr&keywords=%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%A0%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E3%80%80%E5%AE%9F%E8%A1%8C%E8%A8%88%E7%94%BB)
* [Extream programming installed](http://www.amazon.co.jp/XP%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%A0%E3%83%BB%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E5%B0%8E%E5%85%A5%E7%B7%A8-XP%E5%AE%9F%E8%B7%B5%E3%81%AE%E6%89%8B%E5%BC%95%E3%81%8D-The-XP-Series/dp/4894714914/ref=sr_1_1?s=books&ie=UTF8&qid=1386502350&sr=1-1&keywords=%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%A0%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E3%80%80%E5%B0%8E%E5%85%A5%E7%B7%A8)
* [Test Driven Development by example](http://www.amazon.co.jp/%E3%83%86%E3%82%B9%E3%83%88%E9%A7%86%E5%8B%95%E9%96%8B%E7%99%BA%E5%85%A5%E9%96%80-%E3%82%B1%E3%83%B3%E3%83%88-%E3%83%99%E3%83%83%E3%82%AF/dp/4894717115/ref=sr_1_2?s=books&ie=UTF8&qid=1386502385&sr=1-2&keywords=Test+Driven+Development+by+example)
* [User stories applied](http://www.amazon.co.jp/User-Stories-Applied-Software-Development-ebook/dp/B0054KOL74/ref=sr_1_cc_1?s=aps&ie=UTF8&qid=1386502435&sr=1-1-catcorr&keywords=User+Stories+applied)
* [Agile Estimating and Planning](http://www.amazon.co.jp/%E3%82%A2%E3%82%B8%E3%83%A3%E3%82%A4%E3%83%AB%E3%81%AA%E8%A6%8B%E7%A9%8D%E3%82%8A%E3%81%A8%E8%A8%88%E7%94%BB%E3%81%A5%E3%81%8F%E3%82%8A-~%E4%BE%A1%E5%80%A4%E3%81%82%E3%82%8B%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E3%82%92%E8%82%B2%E3%81%A6%E3%82%8B%E6%A6%82%E5%BF%B5%E3%81%A8%E6%8A%80%E6%B3%95~-Mike-Cohn/dp/4839924023/ref=sr_1_1?s=books&ie=UTF8&qid=1386502473&sr=1-1&keywords=%E3%82%A2%E3%82%B8%E3%83%A3%E3%82%A4%E3%83%AB%E3%81%AA%E8%A6%8B%E7%A9%8D%E3%82%82%E3%82%8A%E3%81%A8%E8%A8%88%E7%94%BB%E4%BD%9C%E3%82%8A)

*[The Agile Samurai](http://pragprog.com/book/jtrap/the-agile-samurai)* collects the essences of these books. In addition to these concepts, this book add new stuff. 
So it's inception deck. If you want to know about inception deck, read this book. And the session of inception deck was also held at this bootcamp. This is important concept of agile practice.

### Why a hero in this book is called "Samurai"?

The author, Jonathan Rasmusson likes *"[Peaceful Warrior](http://www.amazon.com/Way-Peaceful-Warrior-Changes-Lives/dp/0915811898)"* . Initial title of "Agile samurai" was "Agile peaceful warrior" after this novel title. But it was not grasped by other people who have not read this book. So collaborators recommended him the word, "Samurai" which means same notion as peaceful warrior. "Samurai" is more perspicuous than "peaceful warrior" to the people of all over the world. Master sensei is also only the notion, not real samurai characters who lived in Japan.

### What is the agile practice?

Agile development means the way of keeping feedback under the cooperative environment. To achieve team's goal, taking action requires cooperative environment of your team. All members must have the sense of ownership of their products. This thought makes good mood and necessary environment. But this practice can be accomplished only by your learning with on-the-job training. There is no secret ingredient. It's just you.

### Last but not least

1. Sharing what you learn with others
2. Keep searching the better answers
3. Enjoy!

Enjoy your agile life!