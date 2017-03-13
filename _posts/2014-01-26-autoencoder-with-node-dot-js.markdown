---
layout: post
blog: true
title: "Autoencoder with node.js"
date: 2014-01-26 21:14
comments: true
categories: ["node", "Deep leanring", "autoencoder"]
author: Kai Sasaki
---

[Auto encoder](https://en.wikipedia.org/wiki/Autoencoder) is used for deep learning. Auto encoder extract characteristics of data through
unsupervised learning. This is a kind of newral network. By using an auto encoder, you don't have to
be in trouble with choicing extracting algorithm, or doing yourself. Therefore, in deepleanring field, 
this algorithm is used very actively. There are many implementation such as Python or Java, which are 
used in machine learning frequently, but I cannot find this in nodejs. So this weekend, I wrote autoencoder in nodejs.

<!-- more -->

When I started writing this code, I referred [@yusugomori/DeepLearning](https://github.com/yusugomori/DeepLearning).
I would like to take this opportunity to express my appreciation and gratitude to him for his great code.

[GitHub source](https://github.com/Lewuathe/n42/blob/master/lib/dA.js)

The major linear algebra library is [sylvelster](http://sylvester.jcoglan.com/) in JavaScript. This is simple and user friendly
library. So if you cannot decide which library you should use in JavaScript, I recommend sylvester.


```js
var Matrix = require('sylvester').Matrix;
var Vector = require('sylvester').Vector;
var utils  = require('./utils.js');
var assert = require('assert');
var generator = require('box-muller');

function dA(input, nVisible, nHidden, W, hBias, vBias) {
    var self = this;
    self.input    = input;
    self.nVisible = nVisible;
    self.nHidden  = nHidden;
    // Initialize weight parameter
    self.W     = (W != undefined)? W : Matrix.Random(nVisible, nHidden);

    // Initialize hidden bias parameters
    self.hBias = (hBias != undefined)? hBias : Vector.Zero(nHidden);

    // Initialize visual bias parameters
    self.vBias = (vBias != undefined)? vBias : Vector.Zero(nVisible);

    self.wPrime = self.W.transpose();
}

dA.prototype.getCorruptedInput = function(input, corruptionLevel) {
    // Return noised data
    assert.isTrue(corruptionLevel < 1);
    noised = [];
    for (var i = 0; i < input.rows(); i++) {
        noised.push([]);
        for (var j = 0; j < input.cols(); j++) {
            // generator returns sampling value according to regular gaussian distribution
            noised[i].push((generator() * corruptionLevel + 1.0) * input.e(i+1, j+1));;
        }
    }
    return $M(noised);
}

dA.prototype.getHiddenValues = function(input) {
    var self = this;
    // Calculate plus weight
    var rowValues = input.x(self.W);
    return utils.sigmoid(utils.plusBias(rowValues, self.hBias));
}

dA.prototype.getReconstructedInput = function(hidden) {
    var self = this;
    var rowValues = hidden.x(self.W.transpose());
    return utils.sigmoid(utils.plusBias(rowValues, self.vBias));
}

dA.prototype.train = function(lr, corruptionLevel, input) {
    var self = this;
    self.x = (input != undefined)? input : self.input;
    
    var x = self.x;
    // Noised data
    var tildeX = self.getCorruptedInput(x, corruptionLevel);
    var y = self.getHiddenValues(tildeX);
    var z = self.getReconstructedInput(y);
    
    // Below this line, backpropagation algorithm is used
    var lH2 = x.subtract(z);
    var sigma = lH2.x(self.W);
    var lH1 = [];
    for (var i = 0; i < sigma.rows(); i++) {
        lH1.push([]);
        for (var j = 0; j < sigma.cols(); j++) {
            lH1[i].push(sigma.e(i+1, j+1) * y.e(i+1, j+1) * (1 - y.e(i+1, j+1)));
        }
    }
    lH1 = $M(lH1);


    var lW = tildeX.transpose().x(lH1).add(lH2.transpose().x(y));

    self.W = self.W.add(lW.x(lr));


    self.vBias = self.vBias.add(utils.mean(lH2, 0).x(lr));
    self.hBias = self.hBias.add(utils.mean(lH1, 0).x(lr));
}


dA.prototype.reconstruct = function(x) {
    var self = this;
    var y = self.getHiddenValues(x);
    var z = self.getReconstructedInput(y);
    return z
}
```


## Traning and result

Try auto encoder!!

```
var data = [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0],
];

var da = new dA($M(data), 3, 2);

for (var i = 0; i < 1000; i++) {
    // 0.1 is learning rate which is used gradient decent
    // 0.02 is standard deviation which is used for add noise to original data
    da.train(0.1, 0.02);
}

da.reconstruct($M([[1.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]]));

/*   
 *   Returns 
 *   [0.5055820272991076, 0.9979837957439818, 0.007330556962859083]   
 *   [0.5042481334395964, 0.006342602394604374, 0.9970156469919944]
 *   [0.5055017563352926, 0.9979783271177022, 0.007473069891271281]
 *
 */

```

In general, this auto encoder looks like working properly. I think the error of difference between original data
and reconstructed data was induced by below two points.

* Lack of divergence of training data
* Parameter tuning

I didn't write many training examples. So in spite of many decent times, the parameters
cannot be updated properly. And I skipped parameter tuning completly :)

## Deep learning module

I will make a deep learning module which uses this auto encoder. Please keep follow [n42](https://github.com/Lewuathe/n42)!!


