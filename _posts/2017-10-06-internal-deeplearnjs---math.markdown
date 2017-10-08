---
title: "Internal deeplearnjs - math"
layout: post
date: 2017-10-06 20:47:29 +0900
image: 'images/'
description:
tag: ["math", "deeplearnjs", "DeepLearning", "JavaScript", "TypeScript"]
blog: true
author: "lewuathe"
---


[deeplearnjs](https://github.com/PAIR-code/deeplearnjs) is a new deep learning framework running on browser accelerated by WebGL hardware acceleration as I introduced before in this [post](/try-deeplearn-js.html). I was interested in the library from the beginning and submitted [some patches](https://github.com/PAIR-code/deeplearnjs/commits?author=Lewuathe) including new optimizer implementations. I learned some internal codebase of the library during this process. So I want to explain some points interesting to me in this post. This time is regarding the component about mathematical calculation in deeplearnjs.

## Mathematical calculation

`NDArrayMath` is a component which is responsible for doing a tensor calculation. This class provides kernel interface like `exp`, `add` and convolution etc.  `NDArrayMath` is an abstract component. Actual calculation will be delegated to implementations on CPU and GPU, `NDArrayMathCPU` and `NDArrayMathGPU` respectively. These implementations are delegated from template method of `NDArrayMath` abstract class. 

```typescript
  /**
   * Adds two NDArrays element-wise, A + B. Supports broadcasting.
   * For a stricter version without broadcasting use math.addStrict().
   *
   * @param a The first NDArray to add element-wise.
   * @param b The second NDArray to add element-wise.
   */
  add(a: NDArray, b: NDArray): NDArray {
    util.assertAndGetBroadcastedShape(a.shape, b.shape);
    return this.executeOp('add', () => this.addInternal(a, b));
  }
  protected abstract addInternal(a: NDArray, b: NDArray): NDArray;
```

`NDArrayMathCPU` and `NDArrayMathGPU` should implement `addInternal` method to provide this kernel function in their platform, CPU and GPU. CPU implementation is very simple. 

```typescript
  protected addInternal<T extends NDArray>(a: T, b: T): T {
    return this.scaledArrayAddInternal<T>(Scalar.ONE, a, Scalar.ONE, b);
  }
```

It's delegated to `scaledArrayAddInternal` further. 

```
  protected scaledArrayAddInternal<T extends NDArray>(
      c1: Scalar, a: T, c2: Scalar, b: T): T {
    const newShape = util.assertAndGetBroadcastedShape(a.shape, b.shape);
    const newValues = new Float32Array(util.sizeFromShape(newShape));

    const aValues = a.getValues();
    const bValues = b.getValues();
    const c1Val = c1.get();
    const c2Val = c2.get();
    for (let i = 0; i < newValues.length; ++i) {
      newValues[i] = c1Val * aValues[i % a.size] + c2Val * bValues[i % b.size];
    }
    return NDArray.make(newShape, {values: newValues}) as T;
  }
```

In contrast, understanding GPU implementation may require a little WebGL familiarity. This is the implementation in `NDArrayMathGPU`. 

```typescript
  protected addInternal<T extends NDArray>(a: T, b: T): T {
    const program = new BinaryOpProgram(binaryop_gpu.ADD, a.shape, b.shape);
    return this.compileAndRun<NDArray, T>(program, [a, b]);
  }
```

It writes a shader program in a plain string. `BinaryOpProgram` just keeps the shader source program string and some metadata. `NDArrayMathGPU` compiles the program and send it to GPU through WebGL API. If you are familiar with the shader pipeline of WebGL, it is not so difficult to understand the process. 

`NDArray` is a data treated as a tensor entity in deeplearnjs. If you touch Python numpy, the interface may look similar to numpy array. We learned how to run kernel program in WebGL GPU for now but how deeplearnjs send a data in `NDArray` to GPU? 

The answer is texture. 

## Texture Manager

A data in `NDArray` is copied to GPU frame buffer as a texture. Texture manager is responsible for managing the data in GPU frame buffer. 

```typescript
function createAndConfigureTexture(
    gl: WebGLRenderingContext, width: number, height: number,
    numChannels: number): WebGLTexture {
  webgl_util.validateTextureSize(gl, width, height);
  const texture = webgl_util.createTexture(gl);

  const tex2d = gl.TEXTURE_2D;
  const internalFormat = getTextureInternalFormat(gl, numChannels);
  const format = getTextureFormat(gl, numChannels);
  webgl_util.callAndCheck(gl, () => gl.bindTexture(tex2d, texture));
  webgl_util.callAndCheck(
      gl, () => gl.texParameteri(tex2d, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE));
  webgl_util.callAndCheck(
      gl, () => gl.texParameteri(tex2d, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE));
  webgl_util.callAndCheck(
      gl, () => gl.texParameteri(tex2d, gl.TEXTURE_MIN_FILTER, gl.NEAREST));
  webgl_util.callAndCheck(
      gl, () => gl.texParameteri(tex2d, gl.TEXTURE_MAG_FILTER, gl.NEAREST));
  webgl_util.callAndCheck(
      gl,
      () => gl.texImage2D(
          tex2d, 0, internalFormat, width, height, 0, format, gl.FLOAT, null));
  webgl_util.callAndCheck(gl, () => gl.bindTexture(gl.TEXTURE_2D, null));
  return texture;
}
```

`createAndConfigureTexture` create texture frame buffer and bind it to the context. A frame buffer in a GPU memory space is allocated. Who send the data into that space?

## NDArray 

`runProgram` method in `gpgpu_math.ts` gets inputs and outputs of the program. 

```typescript
const outTex = output.getTexture();
```

`getTexture()` actually copies the data into frame buffer allocated in advance. This is a method in `NDArray`. 

```typescript
  getTexture(preferredShapeRC?: [number, number]): WebGLTexture {
    if (this.data.texture == null) {
      this.uploadToGPU(preferredShapeRC);
    }
    return this.data.texture;
  }
```

Finally it is delegated to `uploadDataToTexture` method in `gpgpu_util.ts`.

```typescript
function uploadDataToTexture(
    gl: WebGLRenderingContext, texture: WebGLTexture, width: number,
    height: number, data: Float32Array, numChannels: number) {
  const textureFormat = getTextureFormat(gl, numChannels);

  webgl_util.validateTextureSize(gl, width, height);
  webgl_util.callAndCheck(gl, () => gl.bindTexture(gl.TEXTURE_2D, texture));
  webgl_util.callAndCheck(
      gl,
      () => gl.texSubImage2D(
          gl.TEXTURE_2D, 0, 0, 0, width, height, textureFormat, gl.FLOAT,
          data));
  webgl_util.callAndCheck(gl, () => gl.bindTexture(gl.TEXTURE_2D, null));
}
```

`gl.bindTexture` send a command to GPU to select the frame buffer allocated in advance for this kernel program.  Then it copies data with `texSubImage2D` command as 2D texture image internally. (But it is 2D tensor actually). So the kernel program can find the data in frame buffer after this method is called. 

## Problem

Copying the data into GPU memory can be an overhead. It is desirable to copy data as much as possible at the same time. The data should not be changed in a batch training in a deeplearning framework. Bulk copying still more important. deeplearnjs now copies the data every time each kernel program runs. There is some room to be improved regarding copying data into GPU memory.
