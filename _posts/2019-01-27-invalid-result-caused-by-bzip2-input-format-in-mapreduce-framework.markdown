---
title: "Invalid result caused by bzip2 input format in MapReduce framework"
layout: post
date: 2019-01-27 19:36:56 +0900
image: 'assets/img/posts/2019-01-27-invalid-result-caused-by-bzip2-input-format-in-mapreduce-framework/catch.png'
description:
tag: ['Hadoop', 'Bug', 'HDFS', 'DistributedSystem', 'Java']
blog: true
author: "Kai Sasaki"
---

It's a story about compression algorithm but not `tar`. 

Although it was an issue a while ago, I'm going to write about [HADOOP-13270](https://issues.apache.org/jira/browse/HADOOP-13270) today because I found it one of the most interesting bug I worked on in Hadoop project. 

Hadoop MapReduce framework has a module called **[InputFormat](https://github.com/apache/hadoop/blob/trunk/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-core/src/main/java/org/apache/hadoop/mapred/InputFormat.java)** which is responsible for reading files in various formats. It can not only read a simple text file line by line and but also supports various kind of serialization formats such as **[Avro](https://avro.apache.org/)**, and compression formats such as gzip.

InputFormat is expected to split one file into several segments called **split** with the method `getSplits`.

```java
InputSplit[] getSplits (JobConf job, int numSplits) throws IOException;
```

Since one mapper reads and processes one split at one time, you can not handle huge files with multiple mappers in a distributed manner unless `InputFormat` knows how to make this split. By splitting the input file into multiple splits, you can run MapReduce efficiently. How to create each split is the key for the efficient MapReduce job. 
Normally, one split is associated with a block of HDFS in order to make use of the locality of the data. That is if the block size is 128 MB, each split tries to read 128MB data. Important things to remember is that **the data read by each split should be readable only by itself**. What does it mean?

Here is the sample file put in HDFS. 

```
...
record(N)
record(N + 1)
record(N + 2)
---- 128 MB ----
record(N + 3)
record(N + 4)
record(N + 5)
...
```

Suppose that there is a file in which each record is written one line as described above. Let's say that reading from the beginning of the file to the record(N + 2) will be exactly 128 MB. In this case, the end of the first split is record(N + 2) and the first record of the next split becomes record(N + 3). But just because the delimiters of records are not always exactly delimited by blocks, you need to expect the case as follows.

```
record(N)
record(N + 1)
reco
---- 128 MB ----
rd(N + 2)
record(N + 3)
record(N + 4)
record(N + 5)
```

Records which cannot be read simply as previously because the boundary of the split is not aligned with the delimiter of records. A mapper does not know how long it can read from the split it is assigned and also does not know whether a split is read correctly by another mapper (perhaps it works on another machine). 
Because of this, InputFormat is the class that is responsible for making readable alignment and makes splits so that records are properly delimited.


# InputFormat with bzip2

However, trying to make a split like this will cause problems in the case of compression format. When it comes to the compressed format such as gzip, files need to be in one split in order to be decompressed. This is incompatible with the purpose of InputFormat. Because it is impossible in principle to divide a compressed file into multiple parts that can be read only by that. In order to read a gzip compressed format with mapper, you need to read the whole part of one file. For example, if you have a 1.2 GB compressed file, it will be 10 blocks and you may want to read it with 10 mappers, but only 1 mapper needs to read all the blocks if it's compressed with gzip. This also loses the locality of the data, and it becomes very inefficient if it is a large file. Such kind of format is called **unsplittable**.

But some compressed formats are splittable. One of them is **[bzip 2](http://www.bzip.org/)**. Bzip2 compresses the file in units that can be divided using a 48-bit approximation value of $$\pi$$ called a **synchronization marker**.

![bzip2](images/posts/2017-03-18-bzip2-hadoop-13270/bzip2.png)

Although the parts written as splits in the above picture are compressed, it can be decompressed by itself They do not depend on each other. In other words, if you read this split, you can read the part with bzip2's uncompressor and you can read it like a normal uncompressed file. You can gain the benefit of distributed processing by using this kind of splittable compression algorithm. (Of course, compression efficiency and compression speed are different in each format, so I think it's better to choose the format that fits your application)

# Invalid result issue filed in HADOOP-13270

Although the introduction has become longer, let's take a look into [HADOOP-13270](https://issues.apache.org/jira/browse/HADOOP-13270). This was a bug that data would be duplicated when we try to read a bzip2 file of a certain size with specific split size.

I found a unit test `TestTextInputFormat.testSplitableCodecs()` failed when the seed is 1313094493.

```java
java.lang.AssertionError: Key in multiple partitions.
at org.junit.Assert.fail (Assert.java: 88)
at org.junit.Assert.assertTrue (Assert.java: 41)
at org.junit.Assert.assertFalse (Assert.java: 64)
at org.apache.hadoop.mapred.TestTextInputFormat.testSplitableCodecs (TestTextInputFormat.java: 223)
```

I do not use bzip2 in my production environment, but if the data is missing or duplicated, the data analysis on top of it is meaningless. That may be a critical bug I thought. And it also seems to be interesting purely. So I tried to find out the cause.

The problem existed in the class named [[Bzip2Codec`](https://github.com/apache/hadoop/blob/9a44a832a99eb967aa4e34338dfa75baf35f9845/hadoop-common-project/hadoop-common/src/main/java/org/apache/hadoop/io/compress/ BZip2Codec.java). This class creates an `InputStream` starting at the most recent marker from the given offset. The original implementation looked like this.

```java
public SplitCompressionInputStream createInputStream(
      InputStream seekableIn, 
      Decompressor decompressor, 
      long start, 
      long end, 
      READ_MODE readMode) throws IOException {
  // I want to find the latest marker that can read the data from start position
  // ...
  // The magic "BZh9" is magic word specially written at the beginning of the file. 
  // Adding a 48-bit marker to this. There are 10 bytes to be searched in total.
  final long FIRST_BZIP2_BLOCK_MARKER_POSITION 
    = CBZip2InputStream.numberOfBytesTillNextMarker(seekableIn);
  long adjStart = 0L;
  // Seek back to where you can find a marker to read
  adjStart = Math.max(0L, start - (FIRST_BZIP2_BLOCK_MARKER_POSITION));
  ((Seekable) seekableIn).seek (adjStart);
  // BZip2CompressionInputStream finds the next marker to read from the adjStart.
  SplitCompressionInputStream in 
    = new BZip2CompressionInputStream (seekableIn, adjStart, end, readMode);
  // ...
}
```

It has already read to the position specified by `start`. Then we want to read the data from the next maker.

![alignment](images/posts/2017-03-18-bzip2-hadoop-13270/alignment.png)

It is necessary to look for the next marker, but since `start` is calculated just in byte units from the end of the previous split, it is possible that the `start` position is in the middle of the marker. If you just let `BZip2CompressionInputStream` seek the next marker, it will find the next marker of the marker we want to find. We need to return back the position a little bit. This is specified by the `adjStart`.

![Adjusted Start](images/posts/2017-03-18-bzip2-hadoop-13270/adjStart.png)

A marker is usually 48 bits (= 6 bytes), but at the beginning of the file, it seems that there is a character "BZh9" and it is 10 bytes in total. That is calculated by `FIRST_BZIP2_BLOCK_MARKER_POSITION` which is 10 bytes. However, "BZh9" is attached only to the beginning of the file. We do not always need to back 10 bytes. This is the case where the problem occurs. The following would be helpful.

![Duplicated records](images/posts/2017-03-18-bzip2-hadoop-13270/read-again.png)

We already read the compressed block containing `start`. But as we went back too far according to the `adjStart`, we found the same marker again. **Data duplication has occurred** here. The cause was simple. Actually, we return 10 bytes where we have to go back only by 6 bytes. The fix itself was simple and it only had to go back 6 bytes in such case. Now the `InputFormat` for bzip2 compression algorithm always returns the consistent result. 

I thought that bugs related to `InputFormat` are critical part once again because they can cause data missing and duplication. But please be relieved. It's an old bug fixed in 2017. If you are using Hadoop 2.7 or later, you can safely use bzip2 InputFormat.

Thanks!

Image: [xkcd: tar](https://xkcd.com/1168/)