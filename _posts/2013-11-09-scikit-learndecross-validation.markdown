---
layout: post
blog: true
title: "scikit-learnでCross Validation"
date: 2013-11-09 21:56
comments: true
categories: ["scikit-learn", "Python", "Cross Validation"]
author: Kai Sasaki
---


だんだんとscikit-learnとMachine Learningに慣れてきた。
今回はCross ValidationとGrid Searchをやってみた。

### Cross Validation

詳しいことは[Wikipedia](http://ja.wikipedia.org/wiki/%E4%BA%A4%E5%B7%AE%E6%A4%9C%E5%AE%9A)に書いてある。
Cross Validationはモデルの妥当性を検証する方法のひとつ。一般的に開発用のデータは訓練データと検証データに分かれる。
しかし、このまま行ってしまうと折角の訓練データが減ってしまうことになる上に、訓練データの選び方によって汎化性能が下がってしまう可能性がある。
Wikipediaに書いてあるもののホールド・アウト検定がこれに当たる。一般にはこれはCross Validationにはあたらない。

ここに書いてあるK-分割交差検定がこれに当たる。K-分割交差検定では開発用のデータをK個に分割しK-1個を訓練用に、残りの一つを検証用に使いモデルの正当性を計算する。
これにより使える訓練データが増えると同時に、これらを訓練データを変えることにより、汎化性能を上げることができる。

scikit-learnで具体的にどのように行うのか書いてみた。訓練に使ったデータとしてはKaggleの[Data Science London](http://www.kaggle.com/c/data-science-london-scikit-learn)で出されているものを用いた。

### SVM

まずは単純にサポートベクターマシンでクラス分けをさせた時のコード

```python
# -*- coding: utf-8 -*-

import os
import sys
from sklearn import svm
import numpy as np
import csv

if __name__ == "__main__":
    train_feature_file = np.genfromtxt(open("../data/train.csv", "rb"), delimiter=",", dtype=float)
    train_label_file = np.genfromtxt(open("../data/trainLabels.csv", "rb"), delimiter=",", dtype=float)

    train_features = []
    train_labels = []
    for train_feature, train_label in zip(train_feature_file, train_label_file):
        train_features.append(train_feature)
        train_labels.append(train_label)

    train_features = np.array(train_features)
    train_labels = np.array(train_labels)

    clf = svm.SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3,gamma=0.001, kernel="rbf", max_iter=-1, probability=False,random_state=None, shrinking=True, tol=0.001, verbose=False)

    clf.fit(train_features, train_labels)

    test_feature_file = np.genfromtxt(open("../data/test.csv", "rb"), delimiter=",", dtype=float)

    test_features = []
    print "Id,Solution"
    i = 1
    for test_feature in test_feature_file:
        print str(i) + "," + str(int(clf.predict(test_feature)[0]))
        i += 1
```

このモデルをCross Validationで検証してみる。

```python
def get_score(clf, train_features, train_labels):
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(train_features, train_labels, test_size=0.4, random_state=0)

    clf.fit(X_train, y_train)
    print clf.score(X_test, y_test) 
```

cross_validation.train_test_splitは一定の割合が検証用データとなるように開発用データを分割する関数。この場合は`test_size=0.4`を指定したので、40%のデータを検証用として使うことになる。
`fit`が60%の訓練データで行うもので、scoreが残された40%のデータで検証を行いその正答率を出してくれる。これがこのモデルの、このテストデータにおける正当性となる。もちろんこれが高ければ高いほどよいが
汎化性能が高いかどうかはここからでは読み取ることができない。そのためK分割を行うことでK回の検証を行うことができる。これらのスコアを平均することで汎化性能も含めたモデルの正当性を表すことができる。

```python
def get_accuracy(clf, train_features, train_labels):
    scores = cross_validation.cross_val_score(clf, train_features, train_labels, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
```

`cross_validation_cross_val_score`でこれらの検証のすべてのscoreを得ることができる。`cv`はK分割の分割の個数を指定することができる。今回は開発用のデータを10個に分割し10回の検証を行う。
scoresには10個のscoreが入ったリストが返ってくる。これの平均をAccuracyとして出している。これで汎化性能も含めたモデルの正当性を得ることができるが、モデルパラメータのチューニングを手で行う必要がある。
手で調整して、Accuracyを計算するというのは非常に手間なのでGrid Searchというアルゴリズムでこのチューニングをある程度自動化することができる。

### Grid Search

パラメータの範囲を指定することで経験的に最適なパラメータの組を探索する方法がGrid Search。Pythonで行うには以下のように書く。

```python
def grid_search(train_features, train_labels):
    param_grid = [
        {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
    ]
    
    clf = GridSearchCV(svm.SVC(C=1), param_grid, n_jobs=-1)
    clf.fit(train_features, train_labels)
    print clf.best_estimator_
```

param_gridに指定することでこの範囲を指定することができる。n_jobsに並列に計算を行うプロセス数を指定することができる。-1を指定するとコア数をデフォルト選ぶようになっている。与えられた訓練データに対してGrid Searchを行う。
時間は少しかかるが、この訓練データに対して最もスコアが高くなるようなモデルパラメータを選ぶことができる。この訓練データを実際のテストデータに使うことができる。

### まとめ

PRMLには実際の機械学習のプロセスみたいなものがあまり細かく書かれていないのでKaggleに提出されているコードとかを実際にみて、こういったプロセスが分かるようになってきた。
あとscikit-learnが便利すぎて、機械学習の学習アルゴリズムだけじゃなくて特徴抽出とかモデルパラメータの最適化なども整備されていたことに驚いた。
