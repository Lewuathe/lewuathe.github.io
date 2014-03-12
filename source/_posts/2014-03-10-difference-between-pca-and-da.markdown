---
layout: post
title: "Difference between PCA and dA"
date: 2014-03-10 22:08:40 +0900
comments: true
categories: ["Machine Learning", "PCA", "dA"]
author: Kai Sasaki
---

Today I gave a presentation about Deep Learning in my office. Through this presentation, I felt
the difficulty of explanation about mathematic notion without equations. Complex concept should
be attached with some equations. Simplicity was one of the biggest purpose of my presentaion.

Anyway, there is a question I cannot answer clearly.

> What's the difference between [PCA](http://en.wikipedia.org/wiki/Principal_component_analysis) and [Denoised Autoencoder](http://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction#Autoencoders)?

It was a difficult question for me. So I studied what distinguished PCA and dA primaly.

<!-- more -->

## PCA

PCA is an abbreviation of principal component analysis. This algorithm is used when you want to reduce the degree of the input data.
Machine learning algorithms might work faster with low degree data. If you don't have a firm reason for using original data, it is better
to reduce the degree from a point of view of performance. In order to work properly with reduced data, processed data should be sparse because
each data point keeps original characteristics for training a valid model. There are two ways mainly, one is the based on maximizing of variance
of original data. This method maximizes below covariance matrix.

<div style="text-align:center" markdown="1">
<img src="/images/posts/2014-03-10-pca-and-sda/covariance.png" />
</div>

This optimization calculation is achieved by obtaining eigenvectors. It is a little slow because of handling matrix.
The second method is based on error minimization way. In advance you define degree reduced data and minimize its difference.

<div style="text-align:center" markdown="1">
<img src="/images/posts/2014-03-10-pca-and-sda/error.png" />
</div>

Both method have below features.

* Making straight projection
* Irreversible
* Extracting characteristics
* O(D^3)

## Denoised autoencoder

Denoised autoencoder is a kind of autoencoder which adds some noise on original data delibarately. Through this process this model
is capable obtaining proper weight for restoring original data. This model is used mainly the field of deep learning.
This autoencoder has below characteristics.

* Making model parameter
* Reversible
* Extracting characteristics
* O(D^2)

## Conclusion

I think the most essential difference between PCA and denoised autoencoder is reversibility. PCA cannot restore original data bacause
it losts the distance from the [principal subspace](http://users.ics.aalto.fi/praiko/papers/pca_iconip/node3.html). On the other hands,
denoised autoencoder keeps its weight matrix inside own model. So it requires only adding transpose matrix of this weight for restoring.
Please let there be no misunderstanding of usability of PCA, the purpose of PCA is not restoring original data. It is improving calculation cost through
degree reduction. Denoised autoencoder must have weight parameter for restoring original data because its output become the input of next layer.
So it has the ability to restore original data.

Though these two algorithms looks same at the first sight, the purposes are different. This produces the different features between PCA and denoised
autoencoder.

Thank you.





