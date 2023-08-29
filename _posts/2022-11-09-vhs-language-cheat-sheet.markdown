---
title: "VHS Language Cheat Sheet"
layout: post
date: 2022-11-09 10:22:56 +0900
image: 'assets/img/posts/2022-11-09-vhs-language-cheat-sheet/catch.jpg'
description:
tag: ['CLI', 'macOS']
blog: true
author: "Kai Sasaki"
---

Many developers who are constantly writing blog posts or giving a presentation at conferences may want a tool to record their terminal screenshots easily like me. In addition, you may wish to be free from the burden of re-recording or editing the demo video many times to adjust the content and format. 

I found [VHS](https://github.com/charmbracelet/vhs) allows us to do that work in a programmable manner. Moreover, it provides a simple programming language to write the scenario shown in the terminal.

For instance, this program can quickly generate the following footage recording the terminal.

```
Output hello.gif

Set FontSize 32 
Set Width 1200
Set Height 600

Type "echo 'Hello, World'"
Sleep 500ms
Enter
Sleep 5s
```

![hello](/assets/img/posts/2022-11-09-vhs-language-cheat-sheet/hello.gif)

This tool is so easy to use that I want to write here the basic usage of VHS as a sort of cheat sheet.

# Basic

First, you write the program in an ordinal text file with the extension `.tape`. After that, you can use any text editor you like. Then `vhs` executes the program and outputs the final artifact in the specified format. 

```
$ vim hello.tape
$ vhs < hello.tape # You will get `hello.gif` file
```

# Available Commands

## Output
Specify file output file. Usable formats are `.gif`, `.mp4`, `.webm`, or a collection of `.png` images.

## Set
Set recording configuration to control the appearance of the terminal. Available subcommands are:

- `Shell`
- `FontSize`
- `FontFamily`
- `Width`
- `Height`
- `LetterSpacing`
- `LineHeight`
- `TypingSpeed`
- `Theme`
- `Padding`
- `Framerate`

`TypingSpeed` controls the global configuration to set the typing speed. A command-based configuration can overwrite it with `@time`. 

```
Set TypingSpeed 0.1
Type "100ms delay per character"
Type@500ms "500ms delay per character"
```

![delay](/assets/img/posts/2022-11-09-vhs-language-cheat-sheet/delay.gif)

You can choose any theme available [here](https://github.com/charmbracelet/vhs/blob/main/THEMES.md).


## Type
Emulate typing. You can launch any other program available in the `$PATH` in the terminal you are running the `vhs`. This feature makes me even happier because there is no need to remember other special commands or syntax. Just typing like I usually do is sufficient. For example, the following tape writes the executable python program in the REPL.

```
Output python_add.gif

Set FontSize 32 
Set Width 1200
Set Height 600

Type "python3"
Sleep 500ms
Enter

Type "def add(x, y):"
Enter
Tab
Type "return x + y"
Enter 2
Sleep 500ms
Type "result = add(1, 3)"
Enter
Type "print(result)"
Enter

Sleep 2s
```

![python add](/assets/img/posts/2022-11-09-vhs-language-cheat-sheet/python_add.gif)

## Cursor Movement
Move cursor `Left`, `Right`, `Up`, and `Down` respectively. You can set the number of types of these cursor movements following the command. The same rule applies to the following special keys as well.

```
Output cursor.gif

Set FontSize 32 
Set Width 1200
Set Height 600

Type "echo 'Hello, World'"
Sleep 500ms
Left 10
Right 8
Left 5
Sleep 5s

```

![cursor](/assets/img/posts/2022-11-09-vhs-language-cheat-sheet/cursor.gif)

## Special Keys
`Backspace`, `Enter`, `Tab`, and `Space` special keys are also available. They are especially critical to write the program in the VHS environment.

## Control Key
Ctrl+<char> provides us a way to type control + key stuff. 

## Sleep
Wait for a certain amount of time.

## Showing/Hiding Type Movement
`Hide` is helpful to keep the typing command from being recorded. This type of command may include some prerequisites or cleanup commands in this category. Note that the final thing we type is shown with `Hide` but not capturing frames. Exiting from the non-capturing mode, we can use `Show`.

![python execute](/assets/img/posts/2022-11-09-vhs-language-cheat-sheet/python_execute.gif)

# Recap

VHS is just a programming language, so we can build up some valuable tools running on top of it. That will accelerate our blog writing or demo preparation significantly.