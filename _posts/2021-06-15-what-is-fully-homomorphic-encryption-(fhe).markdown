---
title: "What is Fully Homomorphic Encryption (FHE)?"
layout: post
date: 2021-06-15 14:34:48 +0900
image: 'assets/img/posts/2021-06-15-what-is-fully-homomorphic-encryption-(fhe)/catch.jpg'
description:
tag: ['CS', 'Cryptography', 'Software', 'Algorithm']
blog: true
author: "Kai Sasaki"
---

Achieving end-to-end privacy is always challenging. It is common to encrypt the users' data as much as possible to keep it secret. But we have thought it is inevitable for us to decrypt the given data at some point to accomplish meaningful computation from that.

Today, I found an interesting library published by Google.

**[google/fully-homomorphic-encryption](https://github.com/google/fully-homomorphic-encryption)**

[Homomorphic encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption) is a technology that allows us to manipulate the data without decrypting it first. The result of the computation on the homomorphically encrypted data is identical to the output without any encryption. This programming paradigm changes the way we think about the computation on encrypted data. It enables us to do specific calculations while preserving privacy end-to-end.

The repository only contains the following library for now.

[FHE C++ transpiler](https://github.com/google/fully-homomorphic-encryption/tree/main/transpiler)

Although the library is just an exploratory PoC status, the notion this technology aims to prove is very impressive to me.

# Reference

* [google/fully-homomorphic-encryption](https://github.com/google/fully-homomorphic-encryption)
* [Homomorphic encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption)
