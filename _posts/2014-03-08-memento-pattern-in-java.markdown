---
layout: post
blog: true
title: "Memento pattern in Java"
date: 2014-03-08 00:02:29 +0900
comments: true
categories: ["Java", "Design Pattern", "Memento"]
author: Kai Sasaki
---

Recently, I implemented some design patterns following [this book](http://www.amazon.co.jp/%E5%A2%97%E8%A3%9C%E6%94%B9%E8%A8%82%E7%89%88Java%E8%A8%80%E8%AA%9E%E3%81%A7%E5%AD%A6%E3%81%B6%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3%E5%85%A5%E9%96%80-%E7%B5%90%E5%9F%8E-%E6%B5%A9/dp/4797327030). This book introduces 23 design patterns that all programmers should know when you write according to OOP instructions. So now I want to write this article about some of these patterns and explain these. All codes that used in this article are put [here](https://github.com/Lewuathe/java-GoF/tree/master/Memento)

<!-- more -->

## What is Memento pattern?

Memento pattern is used for recording past statuses and for recovering susequently. For example when you use text editor such as vim or emacs, do you use `undo`?
Why do you think this `undo` command can perform? As one way, all statuses(sometimes not all) are recorded as a type of object. Then you can recover this object
to use this recovered data in your application. Let's picking up game example, examine the structure of memento pattern.

## Main

```java
import game.Gamer;
import game.Memento;

public class Main {
    public static void main(String[] args) {
    Gamer gamer = new Gamer(100);
    Memento memento = gamer.createMemento();
        for (int i = 0; i < 100; i++) {
            System.out.println("=== " + i);
            System.out.println("Current: " + gamer);
            gamer.bet();
            System.out.println("Money: ¥" + gamer.getMoney());

            if (gamer.getMoney() > memento.getMoney()) {
                System.out.println("Save current state");
                memento = gamer.createMemento();
            } else if (gamer.getMoney() < memento.getMoney() / 2) {
                System.out.println("Restore previous state");
                gamer.restoreMemento(memento);
            }

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {

            }
            System.out.println("");
        }
    }
}
```


On every turn, a gamer bets and gets money or some fruits. If you get more money at the last of game you win. It's very simple.
Please pay attention to line 7. Mement pattern is used there. This memento object is used when gamer can get more money or reduce
his money to half of previous one. For saving, call `gamer.createMemento()` and for restoring, call `gamer.restoreMemento()`.
All concepts that are included in memento pattern are these. It is easy to understand this pattern. Do you think you can write this pattern
in your production code tomorrow? Please try it.

As a reference, memento class is also placed here. But it is not core concept of memento pattern. You can arrange this concrete logic for your use
if you could only save and restore statuses.

```java
package game;

import java.util.ArrayList;
import java.util.List;

public class Memento {
    int money;
    ArrayList fruits;

    public int getMoney() {
	        return money;
    }

    public Memento(int money) {
        this.money = money;
        this.fruits = new ArrayList();
    }

    void addFruit(String fruit) {
        fruits.add(fruit);
    }

    public List getFruits() {
        return (List)fruits.clone();
    }
}
```

Is there any unclear stuff? Please look into [this codes](https://github.com/Lewuathe/java-GoF/tree/master/Memento).

Thank you.
