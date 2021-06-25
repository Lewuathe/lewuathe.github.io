---
title: "What is FMA (Fused multiply-add)"
layout: post
date: 2021-06-25 14:48:24 +0900
image: 'assets/img/posts/2021-06-18-what-is-fma-(fused-multiply-add)/catch.jpg'
description:
tag: ['CPU', 'Compiler', 'Math']
blog: true
author: "Kai Sasaki"
---

FMA (Fused multiply-add) is a technical term representing the floating-point operation performed multiplication and addition in one step. This operation executes the following arithmetic calculation, which frequently shows up in various programs. Unlike separating multiplication and additional operation, it achieves higher performance and numerical precisions.

$
r = (a * b) + c
$

For instance, x86 provides [FMA instruction set](https://en.wikipedia.org/wiki/FMA_instruction_set) as streaming SIMD extensions for 128 and 256 bits. This instruction is helpful to achieve better performance for machine learning applications requiring many intensive numerical calculations.

This unit is counted to estimate the number of flowing point instructions necessary to compute the state-of-the-art machine learning models.

[albanie/convnet-burden](https://github.com/albanie/convnet-burden)

# Reference

- [Fused multiply–add](https://en.wikipedia.org/wiki/Multiply%E2%80%93accumulate_operation#Fused_multiply%E2%80%93add)
- [FMA Instruction Set](https://en.wikipedia.org/wiki/FMA_instruction_set)
