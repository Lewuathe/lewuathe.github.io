---
layout: post
title: "Case class for Swift"
date: 2014-06-19 19:15:40 +0900
comments: true
categories: ["Swift", "Scala", "Case class"]
author: Kai Sasaki
---

Last week, Apple new programming language [Swift](https://developer.apple.com/swift/) was released.
From that time I keep considering Swift looks like [Scala](http://www.scala-lang.org/) language.
Scala has two sides as object-oriented-language and functional-programming-language. So there are many features
you should learn from scala. One of the most powerful feature of scala is pattern matching. This feature in scala context
can be applied to all type objects. It is called constructor pattern matching.

<!-- more -->

```scala
case class User(name: String, age: Int) {}

val u = User("NOBITA", 12)

val ret = u match {
    case User("TAKESHI", 12) => 1
    case User("NOBITA", 12)  => 2
    case User("NOBITA", 13)  => 3
    case _ => 4
}

// ret is 2
```

All you should do to use pattern match with your custom class is declare `case` class.
The scala compiler generates `unapply` method called extractors automatically. So you can use
these feature very easily.

So Swift is also functional programming language. And it has pattern matchin with `switch` control flow. But I think it is not sufficient in comparison with Scala.

Therefore I tried it.

```
//
//  SwiftCase.swift
//  SwiftCase
//
//  Created by Sasaki Kai on 6/19/14.
//  Copyright (c) 2014 Sasaki Kai. All rights reserved.
//

import Foundation


// For matching, unapply method is necessary
protocol SwiftCase {
    func unapply() -> Array<NSObject>
}

class SwiftPair {
    let first: SwiftCase
    let second: AnyObject
    init(first: SwiftCase, second: AnyObject) {
        self.first = first
        self.second = second
    }
}

// DSL like logic for generating pair (Matching object, Result object)
@infix func ~> (source: SwiftCase, target: AnyObject)-> SwiftPair {
    return SwiftPair(first: source, second: target)
}

func match(c: SwiftCase)(arr: Array<SwiftPair>)-> AnyObject? {
    for pair in arr {
        let matchArr = (pair.first as SwiftCase).unapply()
        let originArr = c.unapply()
        var isOk = true
        if matchArr.count == originArr.count {
           for var i = 0; i < matchArr.count; ++i {
                if matchArr[i] != originArr[i] {
                    isOk = false
                }
           }
           if isOk {
              return pair.second
           }
        }
    }
    return nil
}
```

With this class and functions, you can write below code.

```
class User: SwiftCase {
    let name: String
    let age: Int
    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }

    func unapply() -> Array<NSObject> {
        return [self.name, self.age]
    }
}

class OtherUser: SwiftCase {
    let name: String
    let age: Int
    let address: String
    init(name: String, age: Int, address: String) {
       self.name = name
       self.age = age
       self.address = address
    }

    func unapply() -> Array<NSObject> {
        return [self.name, self.age, self.address]
    }
}

let user = User(name: "NOBITA", age: 34)
let ret : AnyObject? = match(user)(arr: [
    User(name: "TAKESHI", age: 23) ~> 1,
    User(name: "NOBITA", age: 32) ~> 2,
    User(name: "NOBITA", age: 34) ~> 3,
    OtherUser(name: "NOBITA", age: 20, address: "TOKYO") ~> 4
])

// ret is 3
```

Is it looks like matching DSL in Swift? So I want to make this class more sophisticated. Some symbols are not easy to understand
and match function need to receive `Array` parameter. It is not cool ;(

The repository is [here](https://github.com/Lewuathe/SwiftCase). If you have some advice, please let me know.
Thank you.

