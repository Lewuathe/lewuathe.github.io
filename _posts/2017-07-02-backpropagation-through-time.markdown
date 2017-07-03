---
title: "Backpropagation Through Time"
layout: post
date: 2017-07-02 19:49:54 +0900
image: 'images/'
description:
tag: ["Deep Learning", "RNN"]
blog: true
author: "lewuathe"
---

Neural Networkにおいて最適化の中心を担うのは[Backpropagation(誤差逆伝播法)](https://en.wikipedia.org/wiki/Backpropagation)ですが、Recurrent Neural Networkではどのように計算されるのかよくわからなかったので、まとめてみました。

# モデル

最もシンプルなRNNを考えます。入力は`x(0), x(1),...,x(t)`の系列でそれぞれが多次元ベクトルです。

![model](images/posts/2017-07-02-backpropagation-through-time/model.png)

このときこのRNNの出力は下記のように記述されます。$$f$$と$$g$$はそれぞれsigmoid関数などの非線形な活性化関数とします。現在の隠れ層の入力は現在の入力$$x(t)$$と一つ前の時刻の隠れ層の値にそれぞれ重みをかけ、バイアスを加えたものになります。これに活性化関数を通したものが隠れ層の出力になります。

\begin{equation}
\boldsymbol{h}(t) = f(U \boldsymbol{x}(t) + W \boldsymbol{h}(t-1) + \boldsymbol{b})
\end{equation}

Network全体の出力は通常と同じように隠れ層の出力に重みをかけ、バイアスを加えてものを活性化関数に与えた出力になります。

\begin{equation}
\boldsymbol{y}(t) = g(V \boldsymbol{h}(t) + \boldsymbol{c})
\end{equation}

この時学習すべきパラメタは$$U$$, $$V$$, $$W$$, $$b$$, $$c$$で大きさは下記のようになります。入力、隠れ層、出力の大きさはそれぞれ`n_in`, `n_hidden`, `n_out`で表しています。

![params](images/posts/2017-07-02-backpropagation-through-time/params.png)


$$V$$, $$c$$に関しては過去からの影響を直接受けないので通常のBackpropagationと同様に計算できそうですが、他のパラメタはどうでしょうか。ここで使うアルゴリズムが[Backpropagation Through Time (BPTT)](https://en.wikipedia.org/wiki/Backpropagation_through_time)です。

# BPTT

まず各層で活性化関数に通す前の値を抜き出してみます。

\begin{equation}
\hat{\boldsymbol{h}}(t) = U \boldsymbol{x}(t) + W \boldsymbol{h}(t-1) + \boldsymbol{b}
\end{equation}

\begin{equation}
\hat{\boldsymbol{y}}(t) = V \boldsymbol{h}(t) + \boldsymbol{c}
\end{equation}

最適化すべき誤差関数を$$E$$として、各層での誤差項を下記のように定義します。

\begin{equation}
\boldsymbol{e_h} (t) := \frac{\partial{E}}{\partial{\hat{\boldsymbol{h}}(t)}}
\end{equation}

\begin{equation}
\boldsymbol{e_y} (t) := \frac{\partial{E}}{\partial{\hat{\boldsymbol{y}}(t)}}
\end{equation}

このように定義すると誤差関数に対する各パラメタの勾配は微分の連鎖律を使って下記のように表すことができます。

\begin{equation}
\frac{\partial{E}}{\partial{U}} = \frac{\partial{E}}{\partial{\hat{\boldsymbol{h}}(t)}} \left(\frac{\partial{\hat{\boldsymbol{h}}(t)}}{\partial{U}} \right)^T = \boldsymbol{e_h} (t) \boldsymbol{x} (t)^T
\end{equation}

\begin{equation}
\frac{\partial{E}}{\partial{V}} = \frac{\partial{E}}{\partial{\hat{\boldsymbol{y}}(t)}} \left(\frac{\partial{\hat{\boldsymbol{y}}(t)}}{\partial{V}} \right)^T = \boldsymbol{e_y} (t) \boldsymbol{h} (t)^T
\end{equation}

\begin{equation}
\frac{\partial{E}}{\partial{W}} = \frac{\partial{E}}{\partial{\hat{\boldsymbol{h}}(t)}} \left(\frac{\partial{\hat{\boldsymbol{h}}(t)}}{\partial{W}} \right)^T = \boldsymbol{e_h} (t) \boldsymbol{h} (t-1)^T
\end{equation}

\begin{equation}
\frac{\partial{E}}{\partial{\boldsymbol{b}}} = \frac{\partial{E}}{\partial{\hat{\boldsymbol{h}}(t)}} \frac{\partial{\hat{\boldsymbol{h}}(t)}}{\partial{\boldsymbol{b}}} = \boldsymbol{e_h} (t)
\end{equation}


\begin{equation}
\frac{\partial{E}}{\partial{\boldsymbol{c}}} = \frac{\partial{E}}{\partial{\hat{\boldsymbol{y}}(t)}} \frac{\partial{\hat{\boldsymbol{y}}(t)}}{\partial{\boldsymbol{c}}} = \boldsymbol{e_y} (t)
\end{equation}

それぞれ誤差項とその層での入力との積というBackpropagationでよくみる形になります。よって$$\boldsymbol{e_h} (t)$$と$$\boldsymbol{e_y} (t)$$をうまく求めてあげればよいことになります。

ここで$$E$$を2乗和誤差関数とすると

\begin{equation}
E = \frac{1}{2} (\boldsymbol{y}(t) - \boldsymbol{t}(t))^2
\end{equation}

出力層の誤差項は$$\boldsymbol{y}(t) = g(\hat{\boldsymbol{y}(t)}) $$であることに注意すると下記のようになります。

\begin{equation}
\boldsymbol{e_y} (t) = \frac{\partial{E}}{\partial{\hat{\boldsymbol{y}}(t)}} = g \prime (\hat{\boldsymbol{y}}(t)) (\boldsymbol{y}(t) - \boldsymbol{t}(t))
\end{equation}

隠れ層での誤差項も同様に

\begin{equation}
\boldsymbol{e_h} (t) = \frac{\partial{E}}{\partial{\hat{\boldsymbol{h}}(t)}} = f \prime (\hat{\boldsymbol{h}}(t)) V^T \boldsymbol{e_y}(t)
\end{equation}

となります。ここまでは通常のBackpropagationとほぼ同じ計算でしたが、RNNでは$$\boldsymbol{h}(t)$$が$$\boldsymbol{h}(t-1)$$に依存しているため誤差も過去に遡って伝播させる必要があります。

![bptt](images/posts/2017-07-02-backpropagation-through-time/bptt.png)

過去からの入力は$$W$$, $$U$$, $$b$$に依存しているので過去からの寄与も含めて更新しなければいけません。ではどうすればいいか。

それぞれの勾配計算の式をみるとすべて$$\boldsymbol{e_h}(t)$$に依存しているので、こいつを計算してやればよさそうです。

\begin{equation}
\frac{\partial{E}}{\partial{U}} = \boldsymbol{e_h} (t) \boldsymbol{x} (t)^T
\end{equation}

\begin{equation}
\frac{\partial{E}}{\partial{W}} = \boldsymbol{e_h} (t) \boldsymbol{h} (t-1)^T
\end{equation}

\begin{equation}
\frac{\partial{E}}{\partial{\boldsymbol{b}}} = \boldsymbol{e_h} (t)
\end{equation}

ただ過去にも誤差項を伝播させていきたいので、$$\boldsymbol{e_h}(t)$$で$$\boldsymbol{e_h}(t-1)$$を表すことを目指します。時刻$$t-1$$における誤差項は

\begin{equation}
\boldsymbol{e_h}(t-1) = \frac{\partial{E}}{\partial{\hat{\boldsymbol{h}}(t-1)}}
\end{equation}

となるので再帰的に

\begin{eqnarray}
\boldsymbol{e_h}(t-1) &=& \frac{\partial{E}}{\partial{\hat{\boldsymbol{h}}(t)}}\frac{\partial{\hat{\boldsymbol{h}}(t)}}{\partial{\hat{\boldsymbol{h}}(t-1)}} \\
&=& \boldsymbol{e_h}(t) \left( \frac{\partial \hat{\boldsymbol{h}}(t)}{\partial \boldsymbol{h}(t-1)} \frac{\partial \boldsymbol{h}(t-1)}{\partial \hat{\boldsymbol{h}}(t-1)} \right)
&=& \boldsymbol{e_h}(t) (W f \prime (\hat{\boldsymbol{h}}(t-1)))
\end{eqnarray}

と求められます。(MathjaxのAlignが効かない。。。)　よって一般的には以下のように書き下せます。

\begin{equation}
\boldsymbol{e_h}(t-z-1) = \boldsymbol{e_h}(t-z) (W f \prime (\hat{\boldsymbol{h}}(t-z-1)))
\end{equation}

過去の隠れ層への誤差伝播は$$(W f \prime (\hat{\boldsymbol{h}}(t-z-1)))$$の分がかけられて伝わっていくことになります。結果として過去への逆伝播の式も誤差に重みと活性化関数の微分をかける形になりました。

これで$$\boldsymbol{e_h}(t)$$で$$\boldsymbol{e_h}(t-1)$$を表すことができたので、順々に過去の誤差項を求めることができます。あとはこれらの誤差を必要な過去分に渡って足し上げていって勾配にします。最終的に各パラメタの更新分は下記のようになります。

\begin{equation}
U_{t+1} = U_t - \eta \sum_{z=0}^{\tau} \boldsymbol{e_h}(t-z)x(t-z)^T
\end{equation}

\begin{equation}
V_{t+1} = V_t - \eta \boldsymbol{e_y}(t)x(t)^T
\end{equation}

\begin{equation}
W_{t+1} = W_t - \eta \sum_{z=0}^{\tau} \boldsymbol{e_h}(t-z)h(t-z-1)^T
\end{equation}

\begin{equation}
\boldsymbol{b_{t+1}} = \boldsymbol{b_t} - \eta \sum_{z=0}^{\tau} \boldsymbol{e_h}(t-z)
\end{equation}

\begin{equation}
\boldsymbol{c_{t+1}} = \boldsymbol{c_t} - \eta \boldsymbol{e_y}(t)
\end{equation}

$$U$$,$$W$$,$$b$$に関しては過去の分の勾配も足し合わせて更新分にしていることがわかります。$$\tau$$は一般的にどれくらいにすべきでしょうか。理想的には長ければ長い方がよいのですが、現実的には勾配の消失や爆発といった問題を引き起こします。一般的には$$\tau = 10$$~$$100$$くらいがよいようです。より長期にわたる依存関係を考慮に入れたい場合にはLSTMやGRUといったモデルを考えた方がいいかもしれません。

# Reference

* [F.A. Gers, J. Schmidhuber. and F. Cummins. Learning to forget: Continual prediction with LSTM](https://pdfs.semanticscholar.org/1154/0131eae85b2e11d53df7f1360eeb6476e7f4.pdf)
* [Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton. Layer Normalization](https://arxiv.org/abs/1607.06450)
* [Core RNN Cells for use with TensorFlow's core RNN methods](https://www.tensorflow.org/api_guides/python/contrib.rnn#Core_RNN_Cells_for_use_with_TensorFlow_s_core_RNN_methods)
* [deeplearning-tensorflow-keras](https://github.com/yusugomori/deeplearning-tensorflow-keras)
* [詳解 ディープラーニング ~TensorFlow・Kerasによる時系列データ処理~ ](http://amzn.asia/hwRfoUh)
