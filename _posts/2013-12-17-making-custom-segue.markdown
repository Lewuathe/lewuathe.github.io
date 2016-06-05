---
layout: post
blog: true
title: "Making custom segue"
date: 2013-12-17 23:21
comments: true
categories: ["iOS", "Objective-C", "iPhone", "Custom"]
author: Kai Sasaki
---

In developing iOS application, have you wanted to make your own cutomized segue? UIKit provides bare segues such as
`push`, `modal`, `popover` and `replace`. These are useful in any situations. But sometimes I want to make my own transition.
So, I wrote down some tips for making your own custom animation used by segue.

## Make custom segue class

In Xcode, add new files. The name of this class, anything is OK. But you have to set super class `UIStoryboardSegue`. Otherwise storyboard
cannot find this custom class subsequently.

![create](/images/posts/2013-12-17-customsegue/create-segue.png)

In this case, I named `FlipSegue`

```objective-c
#import <UIKit/UIKit.h>

@interface FlipSegue : UIStoryboardSegue

@end
```

And write animations like below.

```
#import "FlipSegue.h"

@implementation FlipSegue

- (void)perform {
    UIViewController *sourceController = (UIViewController*)self.sourceViewController;
    UIViewController *destinationController = (UIViewController*)self.destinationViewController;

    CATransition *transition = [CATransition animation];
    transition.duration = 0.4;
    transition.timingFunction = [CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionEaseInEaseOut];

    // Set transition animation type
    transition.type = kCATransitionFade;
    // Set transition animation subtype
    transition.subtype = kCATransitionFromTop;
    
    // Change animation
    [sourceController.navigationController.view.layer addAnimation:transition forKey:@"mytransition"];
    
    // Transition 
    [sourceController.navigationController pushViewController:destinationController animated:NO];

}

@end
```

When this segue is called, these animation settings are executed automatically. If you want to change animation, `type` and `subtype` is the core
of how the animation moves. These presets are documented in [here](https://developer.apple.com/library/ios/documentation/GraphicsImaging/Reference/CATransition_Class/Introduction/Introduction.html)
Please see official document for detail. And then we'll use this segue on storyboard.

## Make segue with story board

You need to draw your custom segue on storyboard.

![storyboard](/images/posts/2013-12-17-customsegue/storyboard-segue.png)

You can see `flip`, when you drag the arrow of segue on storyboard. This is your custom `FlipSegue`. 
So choose this segue. And run!! Pusing source button of flip segue, your will see your custom animated transition. 

