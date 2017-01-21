---
title: "Introduction of dllib"
layout: post
date: 2017-01-21 23:20:48 +0900
image: 'images/'
description:
tag: ["Deep Learning", "Machine Learning"]
blog: true
jemoji:
author: "lewuathe"
---

I keep thinking about releasing self developed deep learning for a few years. That's a good way to motivate my learning about deep learning. I've already done several time with [n42](https://github.com/Lewuathe/n42) and [neurallib](https://mvnrepository.com/artifact/com.lewuathe/neurallib_2.10). But they are not so much general and hard to extend. So I reinitialize the project re-introduce brand new deep learning framework named [dllib](http://www.lewuathe.com/dllib/).

[![dllib site](/images/posts/2017-01-21-dllib/dllib_site.png)](http://www.lewuathe.com/dllib/)

dllin is a simple deep learning framework running on Apache Spark. The framework was develped to achieve

- Simplicity for extending algorithms
- Easy to learn distributed deep learning algorithms and design
- Compatible Spark ML Dataset based interface

The usage is easy for some developers who are already familiar with existing high level deep learning frameworks such as Keras.

```scala
import com.lewuathe.dllib.graph.Graph
import com.lewuathe.dllib.layer.{AffineLayer, ReLULayer, SoftmaxLayer}
import com.lewuathe.dllib.network.Network

// Define the network structure as calculation graph.
val graph = new Graph(Array(
  new AffineLayer(100, 784),
  new ReLULayer(100, 100),
  new AffineLayer(10, 100),
  new SoftmaxLayer(10, 10)
))

// Model keeps whole network parameters which should be trained.
// Default is in-memory model.
val model = Model(nn3Graph)

val nn3 = Network(model, graph)

// MultilayerPerceptron defines the optimization algorithms and hyper parameters.
val multilayerPerceptron = new MultiLayerPerceptron("MNIST", nn3)

// We can pass Dataset of Spark to the network.
val trainedModel = multilayerPerceptron.fit(df)

val result = trainedModel.transform(df)

result.filter("label = prediction").count()
```

The imporant components to create network are three.

- `Layer`
- `Graph`
- `Model`

`Layer` is a component which specifies a layer of neural network. The layer transforms a vector into another vector one by one. `Graph` specifies the structure of whole network components. So we can create neural network model with adding `Layer`s to `Graph`. One thing to notice is `Layer` and `Graph` have no persistent data in themselves. So parameters to be trained should be given other parts. This is `Model`. Model keeps whole parameters of each `Layer`. So if we want to predict after training, we can give trained `Model` to your network. Though currently we have only in-memory model, we'll implement distributed versions by using parameters server. That must provide high performance with [model parallelism](https://research.google.com/pubs/pub40565.html).

Since dllib is compatible with [Spark ML Dataset based interface](https://spark.apache.org/docs/latest/ml-guide.html), we can easily import existing data into dllib we you already have Spark cluster. Spark ML can be run on local machine as well as distributed mode. You can try with `packages` option immediately.

```
$ ./bin/spark-shell --packages Lewuathe:dllib:0.0.9
```

dllib is uploaded on [Spark packages](https://spark-packages.org/package/Lewuathe/dllib) and [maven central](https://mvnrepository.com/artifact/com.lewuathe/dllib_2.11).

Last but not least, dllib is under development. We'll implement CNN, RNN and other network structure. And also documentation should be enhanced. Please give me any feedback or patches if you are interested. It's my hobby project but I'm very glad if I can cooperate with some developers in the world who are interested in deep learning.

Thank you.
