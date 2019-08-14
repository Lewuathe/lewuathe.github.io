---
title: "VC dimension and predictive loss"
layout: post
date: 2017-07-23 09:26:31 +0900
image: 'assets/img/posts/2017-07-23-vc-dimension-and-predictive-loss/overfitting.png'
description:
tag: ["Machine Learning", "VC Dimension", "Math"]
blog: true
author: "lewuathe"
---

How can we estimate the loss of a machine learning model based on its complexity?
We know that complex model can explain various kinds of data set space but it can overfit
to the sample space. We want to optimize the loss in whole data space instead of sample space.

It means that we need to know the balance between model complexity and the possibility of overfitting.


The prediction by green line model is overfitting to sample data set. It's not enough general. The main purpose of this article to understand the relationship between predictive loss and model complexity.

## Predictive loss and Empirical loss

We want to get a model which is optimized for whole data space. (e.g. all handwritten data) But we cannot observe whole possible data. We only be able to observe the part of them. So only we can do is optimizing the model against observed data not whole data space. The loss function defined on observed data is called **empirical loss**. The one defined on whole data space is called **predictive loss**. The important point here is we cannot calculate true predictive loss never. It is only possible to estimate from empirical loss. Assuming the data set is generated from a probability distribution $$D$$ and loss function we use is $$l(y, \hat{y})$$. The prediction loss of a **hypothesis** is this.

\begin{equation}
R(h) = E_{(X,Y) \sim D} [l(h(X), Y)]
\end{equation}

Hypothesis a predictive function that can be generated from the model. Basically model in this context can be defined as the collection model some hypothesis. This concept is important to define a model complexity later.

Then define empirical loss.

\begin{equation}
\hat{R(h)} = \frac{1}{n} \sum_{i=1}^{n} l(h(X_i), Y_i)
\end{equation}

$$(X_i, Y_i)$$ are observed data generated from probability distribution $$D$$. We can calculate this value with given sampled datasets, but we want to optimize predictive loss to make the model sufficiently general. If our model provides low empirical loss but high predictive loss, our model must be overfitting.

## Bayes rule

The goal of our prediction is finding the hypothesis from the model that provides the minimum predictive loss. In theory predictive loss can have lower limit.

\begin{equation}
inf R(h)
\end{equation}

We call it **Bayes error**. If a hypothesis that provides bayes error, it is called **Bayes rule**. We want to find bayes rule from our model through optimizing process.

## VC dimension

How can we find the relationship between model complexity and these loss values? First we need define *model complexity*. One of the complexity is [**VC dimension**](https://en.wikipedia.org/wiki/VC_dimension) named after [Vapnik](https://en.wikipedia.org/wiki/Vladimir_Vapnik), [Chervonenkis](https://en.wikipedia.org/wiki/Alexey_Chervonenkis). Since VC dimension is used for capturing the characteristics of combination of a set, it's also used theory of combination.

Assuming $$\mathscr{H}$$ is a set of hypothesis. A hypothesis $$h \in \mathscr{H}$$ is a function from input space $$\mathscr{X}$$ to the binary label.

\begin{equation}
h: \mathscr{X} \to \\{ +1,-1 \\}
\end{equation}

The output space of $$h$$ which corresponds to input space $$\mathscr{X}^n$$ is $$\mathscr{Y}^n$$. We define the number of combination of output space like this.

\begin{equation}
\Pi_{\mathscr{H}} (x_1, ..., x_n) = | \\{ (h(x_1), ... h(x_n)) \in \mathscr{Y}^n \\} | h \in \mathscr{H} |
\end{equation}

From this definition, it satisfied below equation.

\begin{equation}
\Pi_{\mathscr{H}} (x_1, ..., x_n) \leq 2^n
\end{equation}

Because the whole pattern $$(h(x_1), ... h(x_n))$$ can generate is less than $$2^n$$. If $$\Pi_{\mathscr{H}} (x_1, ..., x_n) = 2^n$$, we can find a hypothesis that can generate the output satisfying all label assignment of sampled data.

We can also think it may be difficult to find a such hypothesis if the number of samples are increasing. So this is the limit of complexity of the model. VC dimension of the model is defined as this.

\begin{equation}
VCdim(\mathscr{H}) = max \\{ n \in \boldsymbol{N} | max_{x_1,...x_n \in \mathscr{X}} \\ \Pi_{\mathscr{H}} (x_1, ..., x_n) = 2^n \\}
\end{equation}

It means that VC dimension is the max data size where the model can generate a hypothesis that satisfies whole label assignment. If $$d \leq VCdim(\mathscr{H})$$, the training can make a progress finely. The empirical loss should be minimum. But at the same time, it can be overfitting because such model can provides a hypothesis that satisfies noise label assignment too.

## A theorem

In order to provide the upper bound of predictive loss of a hypothesis, it is necessary to set a theorem first.

Assuming, $$VCdim = d < \inf $$, $$(X_1, Y_1), ... ,(X_n, Y_n)$$ is obey i.i.d. $$n \geq d$$.

\begin{equation}
Prob(sup_{h \in \mathscr{H}} | R(h) - \hat{R}(h) | \leq 2 \sqrt{\frac{2d}{n}log \frac{en}{d}} + \sqrt{\frac{log(2/\delta)}{2n}}) \geq 1 - \delta
\end{equation}

It provides the upper bound of the difference between predictive loss and empirical loss with given model, $$\mathscr{H}$$. By using this theorem, we can evaluate the predictive loss of obtained hypothesis from training process.

Assuming sampled data $$ { (X_1, Y_1),...,(X_n, Y_n) } $$ is given. The hypothesis obtained through optimizing empirical loss is $$h_S$$. For simplicity we can assume that bayes rule $$h_0$$ is included in the model $$\mathscr{H}$$. It leads

\begin{equation}
\hat{R}(h_S) \leq \hat{R}(h_0)
\end{equation}

\begin{equation}
R(h_0) \leq R(h_S)
\end{equation}

Then it leads this relationship.

\begin{equation}
R(h_S) \leq \hat{R}(h_0) + R(h_S) - \hat{R}(h_S)
\end{equation}

because $$\hat{R}(h_0) - \hat{R}(h_S) \geq 0$$. The right side can be evaluated as

\begin{equation}
\hat{R}(h_0) + R(h_S) - \hat{R}(h_S) \leq R(h_0) + |R(h_0) - \hat{R}(h_0)| + sup_{h \in \mathscr{H}} |R(h) - \hat{R}(h)|
\end{equation}

because $$a \leq b +\|a - b\|$$ for any b.

\begin{equation}
R(h_0) + |R(h_0) - \hat{R}(h_0)| + sup_{h \in \mathscr{H}} |R(h) - \hat{R}(h)| \leq R(h_0) + 2 sup_{h \in \mathscr{H}} |R(h) - \hat{R}(h)|
\end{equation}

Then it leads below equation with probability $$1-\delta$$ by using previous theorem.

\begin{equation}
R(h_0) + 2 sup_{h \in \mathscr{H}} |R(h) - \hat{R}(h)| \leq R(h_0) + 4 \sqrt{\frac{2d}{n} log \frac{en}{d}} + 2 \sqrt{\frac{log(2/\delta)}{2n}}
\end{equation}

So in total

\begin{equation}
Prob(R(h_S) \leq R(h_0) + 4 \sqrt{\frac{2d}{n} log \frac{en}{d}} + 2 \sqrt{\frac{log(2/\delta)}{2n}}) \leq 1 - \delta
\end{equation}

Please note that $$h_S$$ is obtained through training process of empirical loss. But it shows upper bound of predictive loss of the hypothesis $$h_S$$. By this relationship, we can find,

* If we increase the sample size, $$R(h_S)$$ can be similar to ideal $$R(h_0)$$
* We need to find a optimal value about $$VCDim = d$$ to bound the $$R(h_S)$$ value.
* Predictive loss is basically relates to the ratio of sample size $$n$$ and VC dimension $$d$$.

## Reference

* [Overfitting from wikipedia](https://en.wikipedia.org/wiki/Overfitting)
* [統計的学習理論　MLPシリーズ](https://www.amazon.co.jp/%E7%B5%B1%E8%A8%88%E7%9A%84%E5%AD%A6%E7%BF%92%E7%90%86%E8%AB%96-%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%83%97%E3%83%AD%E3%83%95%E3%82%A7%E3%83%83%E3%82%B7%E3%83%A7%E3%83%8A%E3%83%AB%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA-%E9%87%91%E6%A3%AE-%E6%95%AC%E6%96%87/dp/4061529056)
* [-統計的学習理論の基礎— by 金森敬文](http://www.math.cm.is.nagoya-u.ac.jp/~kanamori/lecture/lec_2015_1st_oosaka-univ/note_03.pdf)
* [VC dimension](https://en.wikipedia.org/wiki/VC_dimension)
