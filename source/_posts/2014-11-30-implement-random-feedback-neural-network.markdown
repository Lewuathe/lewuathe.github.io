---
layout: post
title: "Implement Random Feedback Neural Network"
date: 2014-11-30 16:50:28 +0900
comments: true
categories: ["Neural Network", "Machine Learning"]
author: Kai Sasaki
---

I'm very interested in neural network algorithm such as recurrent neural network, sparse auto encoder, restricted boltzmann machine and so on. Most of neural network learning algorithms are based on [backpropagation](http://en.wikipedia.org/wiki/Backpropagation). This algorithm was first developed in 1974 as the context of neural network. Backpropagation is a simple and efficient learning algorithm. So it seems as a defact standard in machine learning field. 

<!-- more -->

Yesterday, I found an intriguing paper on CUL. This is it. 

<[Random feedback weights support learning in deep neural networks](http://arxiv.org/abs/1411.0247)> 

This paper says error feedback can be passed with random weight which is not totally related to each neuron's weight, even backpropagation passes an error according to the degree of contribution of each neuron. They call this algorithm **Random Feedback**. So the reason why this algorithm works is also described in this paper. If you want to know more detail, I recommend you to read it. Instead I experimented this random feedback algorithm with [my own implementation](https://github.com/Lewuathe/42) and compared backpropagation neural network and random feedback neural network.

## Implementation
In fact, there is almost no difference between backpropagation and random feedback except for only one line. Backpropagation uses own model parameters for feedback. These parameters are updated through iterations, not fixed. This feedback is written as [this](https://github.com/Lewuathe/42/blob/master/src/main/scala/fortytwo/networks/NN.scala#L107).

```scala
for (l <- countOfLayers.length - 2 until 0 by -1) {
  d = actPrimeFunc(zs(l - 1)) :* (weights(l).t * d) // Feedback according its own weight parameters
  ret = (d * activations(l - 1).t, d) :: ret
}
```

On the other hand, random feedback algorithm uses fixed matrix which is generated when object is constructed. This matrix is random and is never updated through iterations. This code is [here](https://github.com/Lewuathe/42/blob/master/src/main/scala/fortytwo/networks/RFNN3.scala#L94)

```scala
for (l <- countOfLayers.length - 2 until 0 by -1) {
  d = actPrimeFunc(zs(l - 1)) :* (fixedDeltaWeights(l).t * d) // Random matrix which is never updated
  ret = (d * activations(l - 1).t, d) :: ret
}
```

`fixedDeltaWeights` are not related to its own model or topology completely. It is generated randomly. But it'll work fine according to this paper. Is it true?

## Experiment

I used [digit recognizer](https://www.kaggle.com/c/digit-recognizer) as a training dataset. This is called MNIST. From this dataset I loaded 10000 training data and 1000 validation data. All codes used this experiment are [here](https://github.com/Lewuathe/42/tree/master/examples/digit-recognizer). And result is [this](http://www.charted.co/?%7B%22dataUrl%22%3A%22https%3A%2F%2Fwww.dropbox.com%2Fs%2Fmumlcg0uwtw7ofb%2Fcomparison_nns.csv%3Fdl%3D0%26raw%3D1%22%2C%22charts%22%3A%5B%7B%22type%22%3A%22line%22%2C%22title%22%3A%22Accuracy%22%2C%22note%22%3A%22This%20chart%20describe%20accuracy%20between%20neural%20network%20which%20uses%20backpropagation%20algorithm%20and%20the%20one%20which%20uses%20random%20feedback%20algorithm%22%7D%5D%7D).

![charts](/images/posts/2014-11-30-implement-random-feedback-neural-network/chart.png)

Dark green represents backpropagation accuracy, light green represents random feedback accuracy. Although random feedback's accuracy was very low on the first part of iterations, this difference disappears as iteration progresses. At last(30 iteration in this experiment), both of these algorithm reached about 90% accuracy. Random feedback seems working! 

## Why?
In order to know the reason random feedback works fine, I run these algorithms as autoencoder. Autoencoder is one type of neural network which is specially trained with unsupervised learning. This type of network is trained to construct input data. So supervised data used by autoencoder is own input data. It is said that this type of network can extract essential characteristics and features of input data. 

![weight](/images/posts/2014-11-30-implement-random-feedback-neural-network/weights.png)

These two images are the result of this training. Both of them represents weight parameter of output layer after 30 iterations. Left weight was trained by backpropagation, and right one was trained by random feedback. Each cell corresponds to one neuron in output layer. In this case there are 10*10 neurons. With looking into these images, I found one thing. There are some neurons which does not learn characteristics of dataset in left one more than right one. This fact may indicate that some neurons don't work through backpropagation feedback. In random feedback process, all neurons can receive error signal independently of its weight parameters. Therefore there might be more neurons that is able to contribute prediction. But I'd like to say it as a particular one of several possibilities and there are no mathematic proofs. 

All codes used this experiment are [here](https://github.com/Lewuathe/42). If you have any questions and feedback, please feel free to send me that. And patches are always welcome. Thank you!
