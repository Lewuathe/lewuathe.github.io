---
layout: post
title: "NN with nodejs"
date: 2014-02-14 22:23
comments: true
categories: ["Newral network", "Machine learning"]
author: Kai Sasaki
---

2 layer newral network is added to [n42](https://github.com/Lewuathe/n42)
This network is simple newral network which can trained throught gradient descent optimization calculation.
It is the same algorithm to the one of denoised autoencoder used by n42. So implementation itself was not diffucult.
The code is showed below.

```js
/**
 *   Training weight parameters with supervised learning
 *
 *   @method train
 *   @param  lr {float}  learning rate
 *   @param  input {Matrix} input data (option)
 *   @param  label {Matrix} label data (option)
 */
NN.prototype.train = function(lr, input, label) {
    var self = this;
    self.x     = (input != undefined)? input : self.input;
    self.label = (label != undefined)? label : self.label;
    
    var x = self.x;
	
	// Get hidden layer value
    var y = self.getHiddenValues(x);

	// The output of this network
    var z = self.getOutput(y);

	// The error of output layer. 
    var lH2 = self.label.subtract(z);

	// Restortion to the error of each hidden layer unit
    var sigma = lH2.x(self.W2.transpose());
    var lH1 = [];
    for (var i = 0; i < sigma.rows(); i++) {
        lH1.push([]);
        for (var j = 0; j < sigma.cols(); j++) {
            lH1[i].push(sigma.e(i+1, j+1) * y.e(i+1, j+1) * (1 - y.e(i+1, j+1)));
        }
    }

	// Make sylvester matrix
    lH1 = $M(lH1);

	// lW1 is the weight matrix from input layer to hidden layer
    var lW1 = x.transpose().x(lH1);

	// lW2 is the weight matrix from hidden layer to output layer
    var lW2 = y.transpose().x(lH2);

	// Add gradient to weight matrix respectively
    self.W1 = self.W1.add(lW1.x(lr));
    self.W2 = self.W2.add(lW2.x(lr));

	// vBias is the input layer bias parameters
    self.vBias = self.vBias.add(utils.mean(lH2, 0).x(lr));

	// hBias is the hidden layer bias parameters
    self.hBias = self.hBias.add(utils.mean(lH1, 0).x(lr));
}
```

Trying.

```
var input = $M([
  [1.0, 1.0, 0.0, 0.0],
  [1.0, 1.0, 0.2, 0.0],
  [1.0, 0.9, 0.1, 0.0],
  [1.0, 0.98, 0.02, 0.0],
  [0.98, 1.0, 0.0, 0.0],
  [0.0, 0.0, 1.0, 1.0],
  [0.0, 0.1, 0.8, 1.0],
  [0.0, 0.0, 0.9, 1.0],
  [0.0, 0.0, 1.0, 0.9],
  [0.0, 0.0, 0.98, 1.0]
]);

var label = $M([
  [1.0, 0.0],
  [1.0, 0.0],
  [1.0, 0.0],
  [1.0, 0.0],
  [1.0, 0.0],
  [0.0, 1.0],
  [0.0, 1.0],
  [0.0, 1.0],
  [0.0, 1.0],
  [0.0, 1.0]
]);

var nn = new NN(input, 4, 10, 2, label);

for (var i = 0; i < 100000; i++) {
  // 0.1 is learning rate
  nn.train(0.1);
}

var data = $M([
  [1.0, 1.0, 0.0, 0.0],
  [0.0, 0.0, 1.0, 1.0]
]);

console.log(nn.predict(data));
// [0.9999597224429988, 0.000040673558435336644]
// [0.0000455181928397141, 0.9999544455271699]
```

## Activation function
This prediction seems rather good, but the activation function was changed to sigmoid function, not softmax function in this case. In the multi class categorizing problem, soft max function usually used to predict. But I can get good result with sigmoid function rather than softmax function. With softmax function, the result is below.

```js
// [0.5242635012777253, 0.47573649872227464]
// [0.2690006890629063, 0.7309993109370937]
```

## Further trying
Umm, this is not the result I want to get. I can't grasp why the result is not correct sufficiently.
I want to keep tracking whether there are any problems in my program.
And with this network, I want to try kaggle mnist problem. Now n42 is run to train mnist data. It takes a lot of time.
If any good result is obtained through this process, I will introduce this blog. Welcome feedback, thank you!!



