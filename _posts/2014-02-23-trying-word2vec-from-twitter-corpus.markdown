---
layout: post
blog: true
title: "Trying word2vec from Twitter corpus"
date: 2014-02-23 17:47:16 +0900
comments: true
categories: ["word2vec", "twitter", "corpus"]
author: Kai Sasaki

---

Do you know [word2vec](https://github.com/dav/word2vec)? This library is one of the hottest module which provides an efficient implementation of the continuous bag-of-words and skip-gram architectures for computing vector representations of words.

Recently, my collegues told me what word2vec is. From that time, I want to try this library in some chance. This time, I trained this skip-gram model with twitter corpus. 

<!-- more -->

## Install word2vec

```
$ git clone https://github.com/dav/word2vec.git
```

There are demo scripts. Let me see demo-word.sh.

```
DATA_DIR=../data
BIN_DIR=../bin
SRC_DIR=../src

TEXT_DATA=$DATA_DIR/text8
VECTOR_DATA=$DATA_DIR/text8-vector.bin

pushd ${SRC_DIR} && make; popd

if [ ! -e $VECTOR_DATA ]; then
  
  if [ ! -e $TEXT_DATA ]; then
    wget http://mattmahoney.net/dc/text8.zip -O $DATA_DIR/text8.gz
    gzip -d $DATA_DIR/text8.gz -f
  fi
  echo -----------------------------------------------------------------------------------------------------
  echo -- Training vectors...
  time $BIN_DIR/word2vec -train $TEXT_DATA -output $VECTOR_DATA -cbow 0 -size 200 -window 5 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 1
  
fi

echo -----------------------------------------------------------------------------------------------------
echo -- distance...

$BIN_DIR/distance $DATA_DIR/$VECTOR_DATA
```

The main part of demo is below.

```
 time $BIN_DIR/word2vec -train $TEXT_DATA -output $VECTOR_DATA -cbow 0 -size 200 -window 5 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 1
```
I found that the only requirement of training data was morphological analyzed text. For example, below.

```
病院
の
待合室
に
い
たら
隣
の
人
が
```

Then how can I make these corpus from twitter API?

## Making twitter corpus

I wrote this script that access twiter search API. In version 1.1, public timeline API has been remove from service.
So you should make corpus from only twitter search API if you want to categorize by language type. Because only search API has 
`lang` parameter. 


```python
# -*- coding: utf-8 -*-

import os
import sys
import twitter
import yaml
import urllib

class TwitterSearch:
    def __init__(self):
        with open('./config.yml', 'r') as f:
            self._config = yaml.load(f)
             
        self._lang = 'ja'
        self._api = twitter.Api(
            consumer_key = self._config["consumer_key"],
            consumer_secret = self._config["consumer_secret"],
            access_token_key = self._config["access_token_key"],
            access_token_secret = self._config["access_token_secret"]
        )
 
    def search(self, word):
        search_word = urllib.quote(word.encode('utf-8'))    # OK
        result = self._api.GetSearch(term=search_word, lang=self._lang)
        for status in result:
            text = status.text.encode('utf-8').replace('\n', '')
            sys.stdout.write(text)
            sys.stdout.write('\n')
  
if __name__ == '__main__':
    words = u'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
    t = TwitterSearch()
    for ch in words:
        t.search(ch)
```


Each line has one tweet text. These texts are searched with japanese syllabary, "あいうえお..." 
in order to make searching logic more simple. But there might be room for improvement in this part. If you want to create more complex search queries, change `words`. 

This script makes such outputs.

```
あ、猫話はあちら様の凛ちゃんの話です。うちの凛ちゃんは鮫なので。あしからず。
あああ乱視＆鳥目でこの時間の外出全然見えないいいいいい
お散歩に行きたくなりますね。あ、今日は猫さんの日なんですね！
あぷりを、いんすとーーるしたぜ。
```

## Morphological analysis

I used [MeCab](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html) for the morphological analysis.


```
$ mecab row_text.txt > morphological_output.txt
```

This library generates below output.


```
病院    名詞,一般,*,*,*,*,病院,ビョウイン,ビョーイン
の      助詞,連体化,*,*,*,*,の,ノ,ノ
待合室  名詞,一般,*,*,*,*,待合室,マチアイシツ,マチアイシツ
に      助詞,格助詞,一般,*,*,*,に,ニ,ニ
い      動詞,自立,*,*,一段,連用形,いる,イ,イ
たら    助動詞,*,*,*,特殊・タ,仮定形,た,タラ,タラ
隣      名詞,一般,*,*,*,*,隣,トナリ,トナリ
の      助詞,連体化,*,*,*,*,の,ノ,ノ
人      名詞,一般,*,*,*,*,人,ヒト,ヒト
が      助詞,格助詞,一般,*,*,*,が,ガ,ガ
「      記号,括弧開,*,*,*,*,「,「,「
あの    連体詞,*,*,*,*,*,あの,アノ,アノ
```

This outputs include a part of speech, and prununciations. So remove it with `awk`.

```
$ awk '{ print $1 }' < morphological_output.txt > words.txt
```

This is output.

```
病院
の
待合室
に
い
たら
隣
の
人
が
```

Ok, now you can train skip-gram algorithm with this data.

## Training

This is my training script.

```sh
DATA_DIR=../data
BIN_DIR=../bin
SRC_DIR=../src

TEXT_DATA=$DATA_DIR/twitter_text
VECTOR_DATA=$DATA_DIR/twitter_text-vector.bin

pushd ${SRC_DIR} && make; popd

echo -- Training vectors...
time $BIN_DIR/word2vec -train $TEXT_DATA -output $VECTOR_DATA -cbow 0 -size 200 -window 5 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 1
  

echo -----------------------------------------------------------------------------------------------------
echo -- distance...

$BIN_DIR/distance $DATA_DIR/$VECTOR_DATA
```

It is the almost same script to `demo-word.sh`. 

Training takes about 3 seconds. It is very short time. (But it means there are not enough training data) :(

```
% ./twitter-script.sh
~/Dropbox/MyWorks/algos/word2vec/src ~/Dropbox/MyWorks/algos/word2vec/scripts
gcc word2vec.c -o ../bin/word2vec -lm -pthread -O2 -Wall -funroll-loops 
gcc word2phrase.c -o ../bin/word2phrase -lm -pthread -O2 -Wall -funroll-loops 
gcc distance.c -o ../bin/distance -lm -pthread -O2 -Wall -funroll-loops 
gcc word-analogy.c -o ../bin/word-analogy -lm -pthread -O2 -Wall -funroll-loops 
gcc compute-accuracy.c -o ../bin/compute-accuracy -lm -pthread -O2 -Wall -funroll-loops 
chmod +x ../scripts/*.sh
~/Dropbox/MyWorks/algos/word2vec/scripts
-- Training vectors...
Starting training using file ../data/twitter_text
Vocab size: 1516
Words in train file: 50979

real    0m0.734s
user    0m1.822s
sys     0m0.076s
-----------------------------------------------------------------------------------------------------
-- distance...
Enter word or sentence (EXIT to break): 
```

Enter some words.


```
Enter word or sentence (EXIT to break):  病院
                                              Word       Cosine distance
------------------------------------------------------------------------
                                               ぶ               0.991685
                                            ソチ                0.990486
                                            bottle              0.989918
                                            点滴                0.988539
```

Word "病院" means hostpital. The forth word that has near vector to hospital is "点滴", an intravenous drip. It looks like word2vec working nice, however other data are irrelevant to hospital. That's too bad.

In addition to this error, cosine distance of all data are above 0.98. These distance points suggest word2vec cannot make sound model with this training data. 
Unfortunately, there are also a lot of words that has no counterpart in training data. In many cases, target words that you want to investigate are not included in this model.
You cannot make use of  this model with such a tiny data extracted from twitter API in practical situation.

## Next

Next time, I want to try with Wikipedia JP corpus. This famous site includes huge corpus data. I am sure to obtain good results in the next time. 

Source codes used this process is [here](https://github.com/Lewuathe/algos/tree/master/word2vec). Please do take a look at these codes!

Thank you.
