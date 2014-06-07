---
layout: post
title: "Heart Bleedを読んだ"
date: 2014-04-08 21:06:12 +0900
comments: true
categories: ["OpenSSL", "Security"]
author: Kai Sasaki
---

今日の日本時間13:00頃、OpenSSLに致命的なバグがあることがわかった。全世界で動いているSSLプロセスが影響を受ける。
簡単に言うと、メモリ上にある任意のデータを漏洩する可能性があるバグだ。
このバグはもう2年も前からあったらしいがGoogle Security TeamのNeel Mentaに見つけられたのはつい最近で、パッチがあたったのは十数時間前だ。

[Add heartbeat extension bounds check.](https://github.com/openssl/openssl/commit/96db9023b881d7cd9f379b0c154650d6c108e9a3)

基本的には[heartbleed.com](http://heartbleed.com/)に詳細が記載されていて、危険なOpenSSLのバージョン、ディストリビューションが書いてある。
対応方法も書いてある。今回はエンジニアとして、コードを読んでどういうバグだったのか理解してみたかったので書いてみる。

<!-- more -->

## 問題の箇所
修正箇所である`ssl/d1_both.c`の該当関数を見てみる。

```c
int
dtls1_process_heartbeat(SSL *s)
    {
    unsigned char *p = &s->s3->rrec.data[0], *pl;
    unsigned short hbtype;
    unsigned int payload;
    unsigned int padding = 16; /* Use minimum padding */


```

heartbeatという機能の詳しいことは調べられていないけれどどうやらクライアントーサーバ型の機能を提供するものらしい。
つまり何らかのリクエストを受け取ってレスポンスを返すようなサービスを提供するものらしい。`dtls1_process_heartbeat`で大事なのは
ポインタ`p`だ。これはリクエストデータを受け取って格納している。このリクエストデータは構造体になっていて、以下のように記述されている。

```c
typedef struct ssl3_record_st
    {
        int type;               /* type of record */
        unsigned int length;    /* How many bytes available */
        unsigned int off;       /* read/write offset into 'buf' */
        unsigned char *data;    /* pointer to the record data */
        unsigned char *input;   /* where the decode bytes are */
        unsigned char *comp;    /* only used with decompression - malloc()ed */
        unsigned long epoch;    /* epoch number, needed by DTLS1 */
        unsigned char seq_num[8]; /* sequence number, needed by DTLS1 */
    } SSL3_RECORD;


```

`data`が実際の受け取っているデータ。このデータは先頭1byteがheart beatのtypeを表し、次の2byteがそのリクエストの長さを表すような
データになっている。これを処理するコードが以下。

```c
/* Read type and payload length first */
hbtype = *p++;
n2s(p, payload);
pl = p;

```

`hbtype`に先頭1byteのheart beatのtypeが格納される。そしてn2sは次の2byteを格納するためのマクロで以下のように定義されている。

```c
/* straight from the openssl source */
#define n2s(c,s)    ((s=(((unsigned int)(c[0]))<< 8)| (((unsigned int)(c[1]))   )),c+=2)
#define s2n(s,c)    ((c[0]=(unsigned char)(((s)>> 8)&0xff), c[1]=(unsigned char)(((s)    )&0xff)),c+=2)
```

`s2n`も後で使うことになる。つまり変数`payload`にはクライアントから受け取ったデータに設定されている、`length`を読み取って格納している。
ここでpayloadには実際に受け取ったデータの長さをチェックして格納されたわけではなく、あくまでもユーザクライアントが送ってきたlengthをそのまま設定していることを覚えておいてほしい。

さて次にレスポンスを返す部分のコードだ。

```c
unsigned char *buffer, *bp;
int r;

/* Allocate memory for the response, size is 1 byte
 * message type, plus 2 bytes payload length, plus
 * payload, plus padding
 */
buffer = OPENSSL_malloc(1 + 2 + payload + padding);
bp = buffer;


```

bufferはレスポンスを返すための実体となるが、ここでの大きさはtype用の1byteとlength用の2byte、そして実データの長さpayloadで設定された大きさ
に余白(これは16byteに設定されている)を合わせて大きさを確保している。実際に走査するときは`bp`を通してとなる。
これに対してレスポンスデータを構築してやる。

```c
/* Enter response type, length and copy payload */
*bp++ = TLS1_HB_RESPONSE;
s2n(payload, bp);
memcpy(bp, pl, payload);


```

リクエストデータと同じようにまず先頭1byteにheart beatのtypeを設定してやる。`TLS1_HB_RESPONSE`だ。そして先程の `n2s`の逆を行うマクロ`s2n`を利用する。
つまり`payload`に設定されている値を`bp`の次の2byteに設定する。そして最後の行がキモだ。

```c
memcpy(bp, pl, payload);

```

先ほどのリクエストから得た`payload`分の長さのデータを`pl`から`bp`にコピーしている。これでレスポンスデータを構築したことになる。
これをユーザクライアントに返すことになるわけだ。

さて今回見つかったバグは既にここまでのコードの中にある。

## バグ
注意して欲しいのは変数`payload`は**ユーザから与えられたデータ**ということだ。つまりだれでも勝手に設定できるため、**正しい値が入っていない**可能性がある。
この場合の正しさというのはリクエストデータの大きさを正しく反映しているかどうかということだ。
もしこの`payload`変数(受け取ったデータの先頭から2byteの値)がデータの長さを正しく反映していない、特に実際のデータ長よりも
長い値が`payload`に設定されているとしたらどうだろう。レスポンスデータを作る以下のコードは正しく動作するだろうか。

```c
memcpy(bp, pl, payload);

```

正しく動作しない。正確にいうと動作に特に影響はないが、余計なものを送ってしまう可能性がある。ここに脆弱性が生まれる。実際の`pl`に入っているデータは`payload`に設定されている値よりも短いため、`pl`から連続したメモリ領域を`bp`に
コピーしてしまう。そして、このあふれた領域にSSL秘密鍵のデータが載っていたらどうだろうか。OpenSSLプロセスであれば秘密鍵のデータをプロセスメモリ上に乗せているのは
十分考えられることだ。
このコピーされてしまったSSL秘密鍵のデータは`bp`を経由してそのままクライアントの手にわたってしまうことになる。
もちろん、最近のコンピュータはプロセスあたりのヒープ領域が大きいため、ただちに秘密鍵の値をコピーしてしまうことにはならないが、やはり可能性はゼロではない。
OpenSSLチームは以下のような修正を加えたパッチを配布している。

## 修正

```c
/* Read type and payload length first */
if (1 + 2 + 16 > s->s3->rrec.length)
    return 0; /* silently discard */
	hbtype = *p++;
	n2s(p, payload);
if (1 + 2 + payload + 16 > s->s3->rrec.length)
    return 0; /* silently discard per RFC 6520 sec. 4 */
	pl = p;


```

安易にユーザの設定したpayload lengthを信用するのではなくチェックをおこなってる。読み取るまえにそもそもデータ長がゼロであれば捨てる。
読み取ったあとも、実際のデータ長さよりも設定されているpayload lengthの方が大きい場合はリクエストを破棄するようにしている。
これで本来読み取られてはいけない部分のデータがレスポンスとして返ることはない。
至ってシンプルなFixだけれど、こういったものでも見逃すことはある。今回のように世界的に影響力のあるソフトウェアに対して優れたエンジニア達が
メンテを行っていてもそうなのだ。自分がコードを書くときの戒めともしたい。

以下を教訓としておこう。

* ちゃんと単体テストを書こう
* Cよりももっとsecureな言語を使おう


参考: [Diagnosis of the OpenSSL Heartbleed Bug](http://blog.existentialize.com/diagnosis-of-the-openssl-heartbleed-bug.html)


