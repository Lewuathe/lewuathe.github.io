---
title: "t-SNE visualization by TensorFlow"
layout: post
date: 2017-06-01 21:46:25 +0900
image: 'images/'
description:
tag: ["TensorFlow", "t-SNE", "PCA"]
blog: true
author: "lewuathe"
---

From TensorFlow 0.12, it provides the functionality for visualizing embedding space of data samples.
It's useful for checking the cluster in embedding by your eyes. Embedding means the way to project a data
into the distributed representation in a space. This technique is often used NLP method and famous by [word2vec](https://www.tensorflow.org/tutorials/word2vec).

Although the detail of word embedding is written [here](http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/), I'll explain briefly.

We have a word dictionary which is encoded in one-hot style.

\begin{equation}
w =
\left[
\begin{array}{rrrrr}
0 & 0 & 0 & 1 & 0
\end{array}
\right]
\end{equation}

$$w$$ represents a word 4th indexed in the dictionary. And we have embedding matrix which can try to convert a word dictionary into 3 dimension embedding space.

\begin{equation}
E =
\left[
  \begin{matrix}
  0.1 & 0.5 & 0.3 \\\
  0.2 & 0.4 & 0.3 \\\
  0.3 & 0.3 & 0.3 \\\
  0.4 & 0.2 & 0.3 \\\
  0.5 & 0.1 & 0.3 				
	\end{matrix}
\right]
\end{equation}

By multiplying them, we have a distributed representation of the word $$w$$.

\begin{equation}
\left[
\begin{array}{rrrrr}
0 & 0 & 0 & 1 & 0
\end{array}
\right]
\left[
  \begin{matrix}
  0.1 & 0.5 & 0.3 \\\
  0.2 & 0.4 & 0.3 \\\
  0.3 & 0.3 & 0.3 \\\
  0.4 & 0.2 & 0.3 \\\
  0.5 & 0.1 & 0.3 				
	\end{matrix}
\right]
=
\left[
\begin{array}{rrr}
0.4 & 0.2 & 0.3
\end{array}
\right]
\end{equation}

The embedded version of the word is useful in terms of these points.

* Provide useful information about the relationship between each words
* Avoid sparse dataset which often require more data to make model more accurate

So converting a word into such continuous vector space is an useful technique. Such embedding matrix can be obtained through the process like word2vec.
In this post, I tried to write a minimal code to visualize the embedding space with given embedding matrix. We can visualize any 2 dimensional matrix but
the format should be like this.

![embedding_matrix](images/posts/2017-06-01-t-sne-visualization-by-tensorflow/embedding_matrix.png)

So first we try to create the dummy embedding matrix with random.

```python
import tensorflow as td
embedding_var = tf.Variable(tf.truncated_normal([100, 10]), name='embedding')
```

In this case, we assume that we have 100 words and it can be converted into 10 dimension space. Please make sure `embedding_var` is made as `Variable`.

Then we visualize this.

```python
from tensorflow.contrib.tensorboard.plugins import projector

with tf.Session() as sess:
    # Create summary writer.
    writer = tf.summary.FileWriter('./graphs/embedding_test', sess.graph)
    # Initialize embedding_var
    sess.run(embedding_var.initializer)
    # Create Projector config
    config = projector.ProjectorConfig()
    # Add embedding visualizer
    embedding = config.embeddings.add()
    # Attache the name 'embedding'
    embedding.tensor_name = embedding_var.name
    # Metafile which is described later
    embedding.metadata_path = './100_vocab.csv'
    # Add writer and config to Projector
    projector.visualize_embeddings(writer, config)
    # Save the model
    saver_embed = tf.train.Saver([embedding_var])
    saver_embed.save(sess, './graphs/embedding_test/embedding_test.ckpt', 1)

writer.close()
```

Summary writer writes a file including necessary information to visualize. It is used by TensorBoard later.
Metafile is used for showing additional data to each words such as word string. Its format should be `csv` and indexed same as embedding matrix.
For example, if we have a word "apple" in 5th position in embedding matrix, the word should also positioned 5th line in `100_vocab.csv`.

```
orange
banana
potate
strawberry
apple
kiwi
...
```

So let's run the program and you will find the directory `./graphs/embedding_test`. Please move `100_vocab.csv` into the directory because we specify
the position of metadata path as relative path.

## TensorBoard

Actually, TensorBoard is a tool for visualizing embedding space. Since it's installed with TensorFlow, you must have it.
TensorBoard refers the log files which is written by previous program statically. It's specified by `--logdir`.

```
$ tensorboard --logdir=graphs/embedding_test
```

![TensorBoard](images/posts/2017-06-01-t-sne-visualization-by-tensorflow/tensorboard.png)

You can see such graph in "EMBEDDINGS" tab in [http://localhost:6006](http://localhost:6006/#embeddings).
The result of PCA is shown as default. Please click T-SNE tab on left side. TensorBoard looks calculating the result in realtime.

<div style='text-align:center;'>
<iframe width="560" height="315" src="https://www.youtube.com/embed/qtNRjfA7xDk" frameborder="0" allowfullscreen></iframe>
</div>

## Reference

* [TensorBoard: Embedding Visualization](https://www.tensorflow.org/get_started/embedding_viz)
* [Vector Representations of Words](https://www.tensorflow.org/tutorials/word2vec)
