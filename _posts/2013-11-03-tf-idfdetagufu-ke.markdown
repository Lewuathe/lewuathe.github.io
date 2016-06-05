---
layout: post
blog: true
title: "TF-IDFでタグ付け"
date: 2013-11-03 22:28
comments: true
categories: ["kaggle", "Machine Learning"]
author: Kai Sasaki
---

Kaggleで挑戦できそうな問題があったのでチャレンジしてみた。

http://www.kaggle.com/c/facebook-recruiting-iii-keyword-extraction

Stack Exchange(Stack Overflowみたいなもの)にあるテキストとそのタグデータを訓練データとして
同様にStack Exchangeにあるページからタグを類推せよという問題。
多分キーワード抽出を行う方法がうまく行くんじゃないかと思いやってみた。

## TF-IDFアルゴリズム

![Equation](/images/posts/2013-11-03-tfidf/equation.png)

基本的にはTF-IDFを使ってみる。これは文書中のtokenの重要度をその頻度と、他の文書にどれくらいないかの指標
の積として表すアルゴリズム。コードで書くと下のような感じ。

```python
import numpy as np
term = <Target Term>
include_document_num = len([d for d in all_documents if term in d])
word_score = term_frequency * np.log( all_document_num / include_document_num)
```

term_frquencyはその文書中にどれくらいその単語が出てきたか。多くの場合は正規化してある。
その後ろの項は全文書中にその単語を含む文書がどれくらいあるかの比の逆数。これは他の文書にその単語がなければないほど大きくなるので、その単語がその文書のキーワードとして十分に機能することを示唆している。
TF-IDFのTFはTerm FrequencyでIDFはInversed Document Frequencyの略だ。

今回はTestデータの各文書の単語として有効な単語(htmlタグや各種記法は省くようにした)についてword_scoreを計算し、その中から正規化されたscoreが10%を超えたものをその文書のキーワードとして抽出するようにしてみた。
プログラムのコアの部分は以下のような形になった。

```python
    # 全テストデータ
    for data in test_file:
	    # テストデータとしてタイトルもあるのでこいつも利用してみる
        title_tokens = nltk.word_tokenize(data[1])

		# 英数字意外の文字を取り除いた
        tokens = re.split(r"\W+", nltk.clean_html(data[2]))

		# ここは自分でかってに付け足した部分。タイトルに含まれる単語達は特別扱いして10個余分に足しておく
		# 本当はここは文書中の何%とかにした方が各文書でのタイトルの重要度にばらつきがでなくていいのかもしれない
        for title_token in title_tokens:
            for i in range(0, 10):
                tokens.append(title_token)

		# 同じ単語のscoreを計算しても意味ないので重複を消しておく
        uniqTokens = set(tokens)

		# 各tokenのscoreを計算。実際の計算はNLTKに任せた
        tf_idf_scores = {}
        for token in uniqTokens:
            tf_idf_scores[token] = collection.tf_idf(token, tokens)

		# scoreでソート
        sorted_tf_idf_scores = sorted(tf_idf_scores.items(), key=lambda x:x[1])

		# 10%を超えたものをkeywordsとして登録
        keywords = [ k for k, v in sorted_tf_idf_scores if v > 0.1]
		# 1個もないのは変なので1番scoreが高いものだけでも抽出しておく
        if len(keywords) <= 0:
            keywords = [ sorted_tf_idf_scores[-1][0] ]

		# ファイル出力
        result_file.write("%s,\"%s\"\n" % (data[0], " ".join(keywords)))
```

訓練データがあまりにもデカイので、ちょっと全部は訓練できない。
一部の訓練データに対して試してみて余分はかなり出てくるけれど、抜けは割りとない。


```
推定キーワード: 1,"an without type file image check uploaded mime"
正解キーワード: 1,"php image-processing file-upload upload mime-types"
```

```
推定キーワード: 2,"How ctrl press prevent firefox closing"
正解キーワード: 2,"firefox"
```

image-processingとか、そもそもそういう単語を文書に含んでなかったらこの方法だと抽出できない。もっと関係抽出とか固有表現認識とかしないといけないかも。あとタイトルの重みを強くし過ぎたせいか"How"とか"Can"とかの単語も結構入ってきてしまう。Stack ExchangeとかStack Overflowって自分が書くときを考えてみてもそうだけど、単純に疑問文書くことも多いから単純にタイトルにキーワードが含まれているだろうという考えは甘いかも。

もう少しチューニングしてみる。あと訓練データが600万件近くあるのでできるだけたくさん利用できるように工夫したい。
(マシンスペックと時間を考えても100万件が今の限界・・・)
