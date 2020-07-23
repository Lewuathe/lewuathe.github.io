---
title: "Longest Prefix Match with Trie Tree"
layout: post
date: 2019-02-12 21:46:58 +0900
image: 'assets/img/posts/2019-02-12-longest-prefix-match-with-trie-tree/catch.png'
description:
tag: ['Algorithm', 'IP', 'Network', 'Trie', 'Tree']
blog: true
author: "Kai Sasaki"
---

The Internet consists of multiple router nodes which decide the destination packet should be sent. Each router on the Internet needs to send the packet to the appropriate target node decided by the given IP destination. But how each router can decide the next destined router with the given IP address?

# Longest Prefix Match

[**Longest prefix match**](https://en.wikipedia.org/wiki/Longest_prefix_match) is an algorithm to lookup the IP prefix which will be the destination of the next hop from the router. The routing table each router stores IP prefix and the corresponding router. This algorithm is used to find the prefix matching the given IP address and returns the corresponding router node. For example, let's consider the following case.

|IP Prefix|Router|
|:---|:---|
|192.168.20.16/28|A|
|192.168.0.0/16|B|

When the given IP address *192.168.20.19* is given, which entries should be picked up? According to the longest prefix match algorithm, node A will be chosen. Because it has a longer subnet mask. The bold numbers are the bits matching the IP address. You can know *192.168.20.16/28* has the longer prefix than *192.168.0.0/16* has. 


|Hex Format|Binary Format|
|:---|:---|
|192.168.20.191|**11000000.10101000.00010100**.10111111|
|192.168.20.16/28|**11000000.10101000.00010100**.00010000|
|192.168.0.0/16|**11000000.10101000.000**00000.00000000|

Generally speaking, the longest prefix match algorithm tries to find the most specific IP prefix in the routing table. This is the longest prefix match algorithm
But looking up the routing table naively is pretty inefficient because it does a linear search in the IP prefix list and picks up the prefix with the longest subnet mask. 
The more entries the routing table has, the longer it takes to lookup. How can we do this more efficient manner?

# Address Lookup Using Trie

Using trie is one solution to find the longest match prefix. [**Trie**](https://en.wikipedia.org/wiki/Trie) is a data structure whose nodes have a part of the prefix. By the nature of the tree data structure, we can search the prefix efficiently by traversing the tree. Let's take a look at the following simple example.

![Lookup with Trie](/assets/img/posts/2019-02-12-longest-prefix-match-with-trie-tree/lookup-with-trie.png)

The left table represents the routing table. This routing table can be described as the right trie tree. Let's say we have *1011* as input. It will be traversed as follows then find the node **C** as the next destination.

![Traverse Trie](/assets/img/posts/2019-02-12-longest-prefix-match-with-trie-tree/traverse-trie.png)

If *1000* comes, **B** will be picked up as the next destination because the node is the last node in the traversed route. Looking up the trie tree is very fast because the number of nodes to be visited is **logarithm order**.

![Traverse Trie 2](/assets/img/posts/2019-02-12-longest-prefix-match-with-trie-tree/traverse-trie2.png)

But using this kind of trie is still inefficient when it comes the number of memory access. It needs to visit up to 32 nodes for each IP address as IPv4 address has 32 bits. It grows more in case of IPv6. That is a huge overhead. 

**Direct Trie** is an alternative to lookup efficiently with a reasonable amount of memory access. Multiple bits are represented by one node in a direct trie. 
By making a node representing several bits, we can reduce the depth of the tree so that looking up needs fewer memory accesses. This is a good resource to learn the direct trie in the longest prefix match. This video is also the reason why I described the algorithm because I'm learning CS6250 in [OMSCS](http://www.omscs.gatech.edu/).

<div style='text-align: center'>
<iframe width="560" height="315" src="https://www.youtube.com/embed/eoltXZ1JXP8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

One drawback of the direct trie is that it consumes a significant amount of memory. As shown in the previous video, it creates 2^8 identical entries when it represents */16 prefixes because entries in the prefix */16 has the same prefix in the first 16 bits. It causes the first level with the same first 16 bits should have the same destination. That will be 2^8 (24 - 16 = 8). Although direct trie enables us to lookup efficiently, it is still a tradeoff problem.

Anyway, the trie is a common data structure used by looking up the longest prefix match IP address in routers on the Internet. If you want to learn the data structures including the comment tree structure, [**Introduction to Algorithms, 3rd Edition**](https://amzn.to/2N3HZ1M) is the best book I've ever read.

<div style='text-align: center'>
<a href="https://www.amazon.com/Introduction-Algorithms-3rd-MIT-Press/dp/0262033844/ref=as_li_ss_il?ie=UTF8&qid=1549979958&sr=8-2&keywords=data+structure&linkCode=li3&tag=lewuathe-20&linkId=be365cf59c624c4668f8446f23add2f4" target="_blank"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=0262033844&Format=_SL250_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=lewuathe-20" ></a><img src="https://ir-na.amazon-adsystem.com/e/ir?t=lewuathe-20&l=li3&o=1&a=0262033844" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</div>

I don't think it's an exaggeration to say it's a bible to learn the algorithm and data structure. It may be an overkill for just learning the tree data structures but I believe it brings you a bunch of insight and fundamental pieces of knowledge about the algorithm and data structures every CS students should learn.

Thanks.


