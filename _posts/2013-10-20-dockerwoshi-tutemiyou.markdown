---
layout: post
blog: true
title: "Dockerで仮想化をはじめよう"
date: 2013-10-20 20:30
comments: true
categories: Docker
author: Kai Sasaki
---

仮想環境構築の方法のひとつに[Docker](http://www.docker.io/)を使ってみた。いままではVirtualBoxを使ってVagrantからつないでいく方法をやってみたけれど、仮想マシンをいちいち立ち上げる方法はどうも遅いのでDockerというもので試してみた。

Dockerの特徴は以下記事から抜粋。

http://apatheia.info/blog/2013/06/17/docker/

* 仮想マシンを立ち上げるわけではなく、ホスト内の隔離された環境で動作するため起動が速い。[LXC](http://linuxcontainers.org/)という技術のことらしい。ここでこの隔離されたシステムのことを **コンテナ** という。
* AUFSを使っている。起動したときはディレクトリを重ねあわせておいて、更新の際に別の場所に書き込むというファイルシステムっぽい。立ち上げ時にイメージコピーがいらないので起動が軽い。

## 動かしてみた

環境は以下で行った

* MacOSX 10.8
* VirtualBox 4.2
* vagrant 1.2.4

他にUbuntu LTS12.04が入ったマシンを持っていたのでVagrant使わずにそっちでトライしたら32bitだとだめらしい。どうもUbuntu日本語コミュニティには32bitイメージしかなかったのでぼけーっと入れたらそっちになってしまったみたい。また入れなおすのもとりあえずめんどくさいのでMacのVagrantにUbuntu仮想マシンを立ち上げてその上にDockerを起動させるという構成。

[ここ](http://docs.docker.io/en/latest/installation/vagrant/)に従えば特に問題なくいけた。

```
$ git clone https://github.com/dotcloud/docker.git
$ cd docker
$ vagrant up
```

ここまでで10minくらいかかる。でも悪いのはVirtualBoxとvagrant。

```
# dockerが起動するか見てみる
$ docker
# サブコマンドがだーっと出る
```

## イメージをダウンロード

```
$ sudo docker pull ubuntu
```

## 先ほどのコンテナ内でスクリプトを動作させる

```
# sudo docker run <実行対象コンテナ> <コマンド(引数あってもいい)>
$ sudo docker run ubuntu /bin/echo hello world
```

別にsudoはなくてもいい
これらはDockerのコンテナ内で実行されているコマンドだが、いまいち仮想ホスト立てている感じにならない。それを感じるためにはDockerをdaemon化させる必要がある。

## コマンドをdaemon化させる

走らせるコマンドを定義する。このコマンドはコンテナのIDを返す。このIDをもとにそのコンテナで何がおきているかを見る
-dはコマンドをdaemon化させるオプション

```
$ CONTAINER_ID=$(sudo docker run -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 1; done")
```

そして起動させる。

```
$ sudo docker logs $CONTAINER_ID
```

さっきのコンテナIDが返ってくるのでこいつを`docker logs`に渡してやると実行されているコマンドの値が見えるようになる。たただしこれは実行が終わったら返ってくるのでリアルタイムにコマンドの結果を見たければ`attach`を使う

```
$ sudo docker attach $CONTAINER_ID
```

ここまで適当にやっていったら、いっぱいコンテナができてしまったので確認してみる。dockerが起動したコマンドたちを確認する場合は`ps`サブコマンドを使う。

```
$ docker ps
ID                  IMAGE               COMMAND                CREATED             STATUS              PORTS
4841794938a7        ubuntu:12.04        /bin/sh -c while tru   7 minutes ago       Up 7 minutes            
79b862e271bc        ubuntu:12.04        /bin/sh -c while tru   8 minutes ago       Up 8 minutes                  
bee9d7a00611        ubuntu:12.04        /bin/sh -c while tru   9 minutes ago       Up 9 minutes           
```

こいつらをとめたければ`stop`を使う

```
$ sudo docker stop 4841794938a7 
4841794938a7 

$ sudo docker ps
ID                  IMAGE               COMMAND                CREATED             STATUS              PORTS
79b862e271bc        ubuntu:12.04        /bin/sh -c while tru   13 minutes ago      Up 13 minutes             
bee9d7a00611        ubuntu:12.04        /bin/sh -c while tru   14 minutes ago      Up 14 minutes                    
```

## まとめ

今回のチュートリアルは[ここ](http://docs.docker.io/en/latest/examples/hello_world/#running-examples)からすべてとった。Dockerかなり簡単だけれど、いまいちコマンドをひとつひとつ打っているだけな気がして仮想マシンをたてて、実行している感じがあまりしない。ここで実際にWebアプリとか作ることとかもできるっぽいのでもうちょっと見ていこうかと。









