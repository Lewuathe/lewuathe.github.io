---
layout: post
title: "Next tile on tempai"
date: 2014-03-19 22:57:59 +0900
comments: true
categories: ["Programming", "Java"]
author: Kai Sasaki
---

I tried [this problem](http://www.itmedia.co.jp/enterprise/articles/1004/03/news002_2.html).

Your program receives the hand of mahjong. Returns the "Waiting style" of this hand.
But there are some conditions as below.

* There are no *Jihai*, only *Manzu*
* Make *Juntsu*, *Kohtsu* and *Head*
* Regard different order waiting as the same
* If there are no waiting, no output

<!-- more -->

My source code are pushed [this repository](https://github.com/Lewuathe/java-GoF/blob/master/AtCoder/MahjongWait/src/Main.java)


```java
import java.util.Scanner;

/**
 * Created by Kai Sasaki on 3/19/14.
 */
public class Main {
    public static void search(int tiles[], boolean isHead, String ans, int order) {
        for (int i = 0; i < 9; i++) {
            if (tiles[i] >= 3) {
			    // In order to remove practical same hands,
				// this operation should be done before bigger values
                if (i + 1 < order) {
                    return;
                }

                // In order to remove practical same hands,
				// this operation should be done before finding head
                if (isHead) {
                    return;
                }

                // Find *Kohtsu*
                int tmp[] = tiles.clone();
                tmp[i] -= 3;
																																								                                 String tmpAns = ans + String.format("(%d%d%d)", i + 1, i + 1, i + 1);
                search(tmp, isHead, tmpAns, i + 1);
            }
        }

        for (int i = 0; i < 7; i++) {
            if (tiles[i] >= 1 && tiles[i + 1] >= 1 && tiles[i + 2] >= 1) {
			    // In order to remove practical same hands,
				// this operation should be done before bigger values
                if (i + 1 < order) {
                    return;
                }

                // In order to remove practical same hands,
				// this operation should be done before finding head
                if (isHead) {
                    return;
                }

                // Find *Juntsu*
                int tmp[] = tiles.clone();
                tmp[i] -= 1;
                tmp[i + 1] -= 1;
                tmp[i + 2] -= 1;
                String tmpAns = ans + String.format("(%d%d%d)", i + 1, i + 2, i + 3);
                search(tmp, isHead, tmpAns, i + 1);
            }
        }

        for (int i = 0; i < 9; i++) {
            if (tiles[i] >= 2 && !isHead) {
                if (i + 1 < order) {
                    return;
                }

                // Find head
                int tmp[] = tiles.clone();
                tmp[i] -= 2;
                String tmpAns = ans + String.format("(%d%d)", i + 1, i + 1);
                search(tmp, true, tmpAns, i + 1);
            }
        }

        // No more mentsu
        int oneCount = 0;
        int twoCount = 0;
        int sum = 0;
        for (int i = 0; i < 9; i++) {
           sum += tiles[i];
           if (tiles[i] == 1) {
               oneCount += 1;
           } else if (tiles[i] == 2) {
               twoCount += 1;
           }
        }

        // 000100000
        if (oneCount == 1 && sum == 1) {
            for (int i = 0; i < 9; i++) {
                if (tiles[i] == 1) {
                    ans += String.format("[%d]", i + 1);
                    System.out.println(ans);
                    return;
                }
            }
        }

        // 000001100
        if (oneCount == 2 && sum == 2) {
            for (int i = 0; i < 8; i++) {
                if (tiles[0] == 1 && tiles[1] == 1) {
                    ans += "[12]";
                    System.out.println(ans);
                    return;
                } else if (tiles[7] == 1 && tiles[8] == 1) {
                    ans += "[89]";
                    System.out.println(ans);
                    return;
                } else if (tiles[i] == 1 && tiles[i + 1] == 1) {
                    ans += String.format("[%d%d]", i + 1, i + 2);
                    System.out.println(ans);
                    return;
                }
           }
        }

        if (twoCount == 1 && sum == 2) {
            for (int i = 0; i < 9; i++) {
                if (tiles[i] == 2) {
                    ans += String.format("[%d%d]", i + 1, i + 1);
                    System.out.println(ans);
                    return;
                }
            }
        }
        return;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Receive string that represents hand values
        String hand = sc.next();

        int tiles[] = new int[9];

        // Initialization
        for (int i = 0; i < 9; i++) {
            tiles[i] = 0;
        }

        // Setting tiles array
        for (int i = 0; i < 13; i++) {
            Integer tile = Integer.parseInt("" + hand.charAt(i));
            tiles[tile - 1] += 1;
        }

        search(tiles, false, "", 1);
    }
}
```

This is the simple depth first search algorithm. Ths main point of this code is in the
main method. I expressed the data structure that represents *Hand* as the interger array.
Each integer corresponds to the count of each tile. So in order to calculate the waiting tile,
in this case, all you have to know is the count of each tile. With this data structure, you don't
need to retain complex structure. And also the operation such as finding *Juntsu* and so on is easy
to execute bacause only increment or decrement of each value of this array.

It took me a long time but thanks to this training, a search algorithm such as [DFS](http://en.wikipedia.org/wiki/Depth-first_search)
is no more alien to me. It's friend!

Thank you.


