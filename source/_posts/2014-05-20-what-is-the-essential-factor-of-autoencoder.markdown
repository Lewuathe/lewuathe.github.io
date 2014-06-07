---
layout: post
title: "What is the essential factor of autoencoder?"
date: 2014-05-20 21:08:45 +0900
comments: true
categories: ["Machine Learning", "Deep Learning"]
author: Kai Sasaki
---

The other day, I wrote neural network which implements backpropagation algorithm.
Following this program I write denoised autoencoder program by inheriting previous neural network.
Backpropagation algorithm is generally good performance in spite of the simplicity. With this code,
I can be ranked in at the [266th(May 20th, 2014)](http://www.kaggle.com/c/digit-recognizer/leaderboard).
So I think this implementation has no bugs. However when I use this program as autoencoder the same is not true.
With autoencoder, you should reduce dimension of input vector in order to extract essential characteristics.
These essential characteristics might be also reduced so it cannot reconstruct the same vector to input vector.
In fact after over-completed this network, I can better performance in terms of the number of accurate answers.

This is code.

<!-- more -->

```java
package com.lewuathe.magi;

import org.ujmp.core.Matrix;

/**
 * Created by sasakiumi on 5/8/14.
 */
public class DenoisedAutoencoder extends NeuralNetwork {
    public double corruptionLevel;

    public DenoisedAutoencoder(int[] numLayers) {
        super(numLayers);
    }

    public DenoisedAutoencoder(int[] numLayers, Matrix w, Matrix b) {
        super(numLayers);
        this.weights[0] = w;
        this.biases[0] = b;
        this.corruptionLevel = 0.2;
    }

    public void setCorruptionLevel(double corruptionLevel) {
        this.corruptionLevel = corruptionLevel;
    }

    /**
     * update
     *
     * @param x
     * @param y
     * @param lr
     */
     @Override
     public void update(double[][] x, double[][] y, double lr) {
          Matrix[] nablaB = new Matrix[2];
          nablaB[0] = Matrix.factory.zeros(numLayers[1], 1);
          nablaB[1] = Matrix.factory.zeros(numLayers[2], 1);
          Matrix[] nablaW = new Matrix[2];
          nablaW[0] = Matrix.factory.zeros(numLayers[1], numLayers[0]);
          nablaW[1] = Matrix.factory.zeros(numLayers[2], numLayers[1]);

          assert x.length == y.length;
          for (int i = 0; i < x.length; i++) {
	            Matrix xMat = Matrix.factory.zeros(numLayers[0], 1);
	            Matrix yMat = Matrix.factory.zeros(numLayers[2], 1);
	            for (int j = 0; j < numLayers[0]; j++) {
	                xMat.setAsDouble(corrupt(x[i][j], corruptionLevel), j, 0);
	            }
                for (int j = 0; j < numLayers[2]; j++) {
	                yMat.setAsDouble(y[i][j], j, 0);
	            }
	            Matrix[][] delta = this.backprod(xMat, yMat);
	            // delta[0]: nablaB
	            // delta[1]: nablaW
	            nablaB[0] = nablaB[0].plus(delta[0][0]);
	            nablaB[1] = nablaB[1].plus(delta[0][1]);
                nablaW[0] = nablaW[0].plus(delta[1][0]);
	            nablaW[1] = nablaW[1].plus(delta[1][1]);
	        }

            // Update biases and weights with gradient descent
	        biases[0] = biases[0].minus(nablaB[0].mtimes(lr));
	        biases[1] = biases[1].minus(nablaB[1].mtimes(lr));
	        weights[0] = weights[0].minus(nablaW[0].mtimes(lr));
            weights[0] = weights[0].minus(nablaW[1].transpose().mtimes(lr));
	}

    @Override
    protected Matrix[][] backprod(Matrix x, Matrix y) {
        Matrix[] nablaB = new Matrix[2];
        nablaB[0] = Matrix.factory.zeros(numLayers[1], 1);
        nablaB[1] = Matrix.factory.zeros(numLayers[2], 1);
        Matrix[] nablaW = new Matrix[2];
        nablaW[0] = Matrix.factory.zeros(numLayers[1], numLayers[0]);
        nablaW[1] = Matrix.factory.zeros(numLayers[2], numLayers[1]);

        // In case of denoised autoencoder, no use of 1st weight layer
        weights[1] = weights[0].transpose();
        // Activation of each layer
        Matrix activation = x;
        // Collection of activation values of each layer including input
        Matrix[] activations = new Matrix[3];
        // Set input activation
        activations[0] = x;
        // Row values before activating
        Matrix zs[] = new Matrix[2];
        for (int i = 0; i < 2; i++) {
            zs[i] = weights[i].mtimes(activation).plus(biases[i]);
            activation = Activation.sigmoid(zs[i]);
            activations[i + 1] = activation;
        }

        // Calculate output layer error
	        Matrix delta = costDerivative(activations[2], y);
	        delta = Util.eachMul(delta, Activation.sigmoidPrime(zs[1]));
	        Matrix L_vbias = delta.clone();
	        nablaB[1] = delta;
            nablaW[1] = delta.mtimes(activations[1].transpose());

            for (int i = 1; i > 0; i--) {
            // Back propagation of output layer error to hidden layers
	            delta = weights[i].transpose().mtimes(delta);
                delta = Util.eachMul(delta, Activation.sigmoidPrime(zs[i - 1]));
	            nablaB[i - 1] = delta;
                nablaW[i - 1] = delta.mtimes(activations[i - 1].transpose());
            }

        Matrix[][] ret = {nablaB, nablaW};
	        return ret;
    }

    private double corrupt(double input, double level) {
	        double noise = level * (2.0 * Math.random() - 1.0);
	        return input * (1.0 + noise);
    }

}

```

Complete code is [here](https://github.com/Lewuathe/magi)
While I contemplates about any bugs or errors hidden in this program, I received good clue.

<div style="text-align:center" markdown="1">
<blockquote class="twitter-tweet" lang="ja"><p><a href="https://twitter.com/Lewuathe">@Lewuathe</a> over-complete autoencoders can often recover interesting structures of the data if regularized (e.g. sparsity constraint)</p>&mdash; Vincent Spruyt (@esurior) <a href="https://twitter.com/esurior/statuses/468730252798492672">2014, 5月 20</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
</div>

I will try it with this clue a little more.

