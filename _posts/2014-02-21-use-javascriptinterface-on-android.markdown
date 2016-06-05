---
layout: post
blog: true
title: "Use JavaScriptInterface on Android"
date: 2014-02-21 21:34:20 +0900
comments: true
categories: ["android", "JavaScript"]
author: Kai Sasaki

---

On Android, there is a system for calling Java method from JavaScript. This is called [JavaScriptInterface](http://developer.android.com/reference/android/webkit/JavascriptInterface.html).
With this class, you can call Java methods run on Android application from JavaScript written on any HTML file.

If you want, you can write good user interface with HTML and JavaScript. And backend logic can be written by Java, Android SDK.
So this is the potential way to write Android application. Today I'd like to introduce this way.

<!-- more -->

## Attach WebView

In order to render HTML, you need to use [WebView](http://developer.android.com/reference/android/webkit/WebView.html). 
So first of all, attach WebView to your layout file.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
              android:orientation="vertical"
              android:layout_width="fill_parent"
              android:layout_height="fill_parent" >

    <WebView
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:id="@+id/webView" 
			android:layout_gravity="center_horizontal"/>
</LinearLayout>
```

## Write you HTML

On previous WebView renders this html file. You need to write this file on your project directory so that an application can use it 
from bundle files. My Sample looks like below.

```html
<!DOCTYPE html>
<html>
<head>
    <title>JSTest</title>
</head>
<body>
    <input type="button" value="Call Java" onclick="JSAction.action()" />
</body>
</html>

```

`JSAction` is the Java class that implements JavaScriptInterface with annotation.
So last let's write down this interface class.


## Write JavaScriptInterface class


```java
public class MyActivity extends Activity {
    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        WebView webView = (WebView) findViewById(R.id.webView);
        webView.setWebViewClient(new WebViewClient());
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);

        webView.addJavascriptInterface(new JavaScriptAction(), "JSAction");
        webView.loadUrl("file:///android_asset/jstest.html");
    }


	// This is the JavaScriptInterface class
	// All you need to do is write annotation for JavaScriptInterface. 
    public class JavaScriptAction {
        @JavascriptInterface
        public void action() {
            Toast.makeText(MyActivity.this, 
			               "Called from JavaScript", 
						   Toast.LENGTH_SHORT).show();
        }
    }
}
```

![demo](/images/posts/2014-02-21-javascriptinterface-android/demo.png)

That's all. When you click input button, a toast will show on screen. 
By using JavaScriptInterface, you can easily separate UI design and business logic. 
Definitely, this will be the useful option for your development. 

If you want to look into the detail of these code, please access [here](https://github.com/Lewuathe/JavaScriptInterface-sample)
This is my sample repository. I'm glad to see this repository is used for further development. 

Thank you.
