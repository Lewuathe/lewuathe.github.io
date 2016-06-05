---
layout: post
blog: true
title: "Training Conditional Random Field"
date: 2014-12-16 12:08:09 +0900
comments: true
categories: ["Machine Learning", "CRF"]
author: Kai Sasaki
---

This article is written as 17th entry of [Qiita machine learning advent calendar](http://qiita.com/advent-calendar/2014/machinelearning).

Conditional random field, CRF, is a kind of discriminative model for sequential data. This model is used widely for labeling natural language sequences such as "I have a pen". There is a motivation to attach tags to this sequence. For example, "I have a pen" can be tagged as "I(Noun) have(Verb) a(Article) pen(Noun)". You can train CRF to predict these tags with given sequential data. CRF is not a forefront algorithm but its knowledges and notions included in CRF must be valuable for understanding a lot of types of probability models. In this entry I'd like to explain the training and prediction process which are used by CRF, especially linear chain CRF.
<!-- more -->

<div style="text-align:center"><img src ="/images/posts/2014-12-16-crf/crf.jpg" /></div>



# Model
CRF is a discriminative model. This model is expressed as below formula.

\begin{equation}
P(\mathbf{y}|\mathbf{x}) = \frac{exp(\mathbf{w} \cdot \psi(\mathbf{x}, \mathbf{y}))}{\sum_{\mathbf{y}} exp(\mathbf{w} \cdot \psi(\mathbf{x}, \mathbf{y}))}
\end{equation}

$\mathbf{y}$ is label data and $\mathbf{x}$ represents sequential data. $\psi$ is a feature function. **Feature function** expresses some features obtained by each sequences. $\mathbf{w}$ is a weight parameter whose factors are correspond to one feature. Usually feature function $\psi$ shows whether particular feature exists or not. When you use linear chain CRF, these features are restricted according to specific rule. This rule makes it easier to update CRF model.

\begin{equation}
\psi("This", "is") = 1
\end{equation}
\begin{equation}
\psi("This", Noun) = 1
\end{equation}

In linear chain CRF, current label($y_i$) only depends on previous label($y_{i-1}$). Current observation data($x_i$) depends on that label($y_i$). Therefore these features can be expresses as below.

\begin{equation}
\psi(y_{i-1}, y_i) = 1
\end{equation}
\begin{equation}
\psi(x_i, y_i) = 1
\end{equation}

First feature function is called "**Transition feature**" and second feature is called "**Observation feature**". Of course these assumptions are too simple to make a perfect model which can express all profound structure of natural language.
But this simple model can be trained within practical time and can give us answers with reasonable accuracy. This is the reason why linear chain CRF is widely used in IME system and so on. The first equation expresses the probability of label(${\mathbf{y}}$) given observations(${\mathbf{x}})$. We want to make CRF be able to return the most valid label sequence with the highest probability. Let me explain how to train this CRF with given sequential data.

# Training
Assume that we are given some training data.

$$
(\mathbf{x}, \mathbf{y}) = (( x_1 , \dots , x_T ), (y_1, \dots , y_T))
$$

In this data, $x_i$ is a observation sequence, $y_i$ is a corresponding label sequence. CRF can be trained through iterative optimization process like most of other machine learning algorithms. So CRF can use SGD or LBFGS methods. In order to optimize CRF we should know the gradient of weight parameters. This gradient can be calculated as below.

\begin{equation}
\Delta \mathbf{w} = \sum_{x^i, y^i} \Bigl( \phi (x^i, y^i) - \sum P(y|x^i) \phi (x^i, y) \Bigr)
\end{equation}

The first term is the sum of all features of given observation data and label sequence. Then the second term is the sum of product of conditional probability of labels given observations and features. This summation can be calculated through all possible patterns of label sequence. When you want to calculate this gradient, the second term can be an obstacle because of its high cost calculation complexity. (Its calculation order increases in proportion to the number of combinations of labels exponentially). We want to reduce the computational complexity of this term. Luckily in the case of linear chain CRF,  **Forward-Backward algorithm** can be applied.

## Forward-Backward Algorithm
The second term can be rewritten.

$$
\sum_t \sum_{y_t, y_{t-1}} \Bigl( P(y_t, y_{t-1}|x) \phi(x, y_t, y_{t-1}) \Bigr)
$$

The first summation is the loop for all sequential points, and the second summation is the loop for all possible labels which is corresponds to $y_t$ and $y_{t-1}$.
In here assume that

$$
\psi(y_t, y_{t-1}) = exp(w \cdot \phi(x, y_t, y_{t-1}))
$$

Therefore

$$
P(y|x) = \frac{\prod_t \psi_t (y_t, y_{t-1})}{Z_{x,w}}
$$

In this equation, $Z$ is regularisation term for making it regarded as probability. So then only we have to do is to marginalize this term,  $P(y\|x)$ for calculating gradient. This term should be marginalized around $y_t$ and $y_{t-1}$ and calculation can be written as below.

$$
P(y_t, y_{t-1}|x) = \sum_{y_{0:t-2}} \sum_{y_{t+1:T+1}} \prod_{t^{'}} \psi_{t^{'}} (y_{t^{'}}, y_{t^{'}-1})
$$

Right term can be analyzed into two parts, before $t-1$ part and after $t$.

$$
\biggl( \sum_{y_{0:t-2}} \prod_{t^{'}=1}^{t-1} \psi_{t^{'}} (y_{t^{'}}, y_{t^{'}-1}) \biggr)
\biggl( \sum_{y_{t+1:T+1}} \prod_{t^{'}=t+1}^{T+1} \psi_{t^{'}} (y_{t^{'}}, y_{t^{'}-1}) \biggr)
$$

For simplification I want to rewrite these terms as below.

$$
\alpha (y_{t-1}, t-1) = \biggl( \sum_{y_{0:t-2}} \prod_{t^{'}=1}^{t-1} \psi_{t^{'}} (y_{t^{'}}, y_{t^{'}-1}) \biggr)
$$

$$
\beta (y_t, t) = \biggl( \sum_{y_{t+1:T+1}} \prod_{t^{'}=t+1}^{T+1} \psi_{t^{'}} (y_{t^{'}}, y_{t^{'}-1}) \biggr)
$$

In this case, $\alpha$ means collection of all features before $t-1$ and $\beta$ means collection of all features after $t+1$. These terms can be calculated recursively as below.

$$
\alpha (y_t, t) = \sum_{y_{t-1}} \phi_t (y_t, y_{t-1}) \alpha (y_{t-1}, t-1)
$$

This is also same to $\beta$ term. You can calculate these terms $\alpha$ and $\beta$ efficiently. By using these terms, marginalised probability can be obtained through this calculation.

I think we've got enough. There is almost nothing to do rest because ordinary optimization logic such as SGD, LBFGS can be applied with these terms. In this post these algorithms does not be explained but it won't hard to understand these.

# Prediction

So now we have a trained model for labeling sequential data. Next and the last step is prediction of labels. Let's look at CRF model again.

\begin{equation}
P(\mathbf{y}|\mathbf{x}) = \frac{exp(\mathbf{w} \cdot \psi(\mathbf{x}, \mathbf{y}))}{\sum_{\mathbf{y}} exp(\mathbf{w} \cdot \psi(\mathbf{x}, \mathbf{y}))}
\end{equation}

To obtain the most probable label, you need to calculate all probability of each label pattern with above model. If each observations can have 2 type labels and sequential length is $N$, all patterns can be count as $2^N$. That number will be increasing exponentially with the number of label types and sequential length. It is hard to calculate it within reasonable waiting time. So there is nice algorithm which can be applied to linear chain CRF prediction. This is one kind of dynamic programming.

## Viterbi Algorithm

A observation probability totally depends on previous observation in sequential line. So only we have to do is to update max probability comparing with previous observations. This algorithm can be formulated as below.

$$
T(t, y_t) = max_t \Bigr[w \psi(x, y_t, y_{t-1}) + T(t-1, y_{t-1}) \Bigl]
$$

$$
S(t, y_t) = argmax_t \Bigr[w \psi(x, y_t, y_{t-1}) + T(t-1, y_{t-1}) \Bigl]
$$

$T(t, y_t)$ represents the max probability of specific observation. $S(t, y_t)$ represents the label which has the max probability in that position. Viterbi algorithm updates these formula through the sequence. This updating is done through sequential observations. Each labels has previous labels which give a max probability to current label. So eventually, we can obtain the labels which give a max probability by returning from the last observation to each previous ones.

Forward-Backward algorithm and Viterbi algorithm look very complex. At first it was too hard for me to understand. That's the reason why I wrote this article. I have a plan to implement a linear chain CRF by myself. I'll write about it another chance. I hope this post will help you understand the piece of CRF notions. Thank you.


# References
* [An Introduction to Conditional Random
Fields for Relational Learning](http://people.cs.umass.edu/~mccallum/papers/crf-tutorial.pdf)
* [日本語入力を支える技術](http://www.amazon.co.jp/%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%82%92%E6%94%AF%E3%81%88%E3%82%8B%E6%8A%80%E8%A1%93-%EF%BD%9E%E5%A4%89%E3%82%8F%E3%82%8A%E7%B6%9A%E3%81%91%E3%82%8B%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC%E3%82%BF%E3%81%A8%E8%A8%80%E8%91%89%E3%81%AE%E4%B8%96%E7%95%8C-WEB-DB-PRESS-plus/dp/4774149934)
* [言語処理のための機械学習入門](http://www.amazon.co.jp/%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E5%85%A5%E9%96%80-%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA-%E9%AB%98%E6%9D%91-%E5%A4%A7%E4%B9%9F/dp/4339027510)
* [Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data](http://www.seas.upenn.edu/~strctlrn/bib/PDF/crf.pdf)
