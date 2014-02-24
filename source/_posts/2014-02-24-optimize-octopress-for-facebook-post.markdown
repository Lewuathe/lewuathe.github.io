---
layout: post
title: "Optimize octopress for facebook post"
date: 2014-02-24 20:25:45 +0900
comments: true
categories: ["octopress", "facebook"]
author: Kai Sasaki

---

This blog made by [octopress](http://octopress.org/), ruby CMS tool. 
As many others do, I also combined this tool with [GitHub pages](http://pages.github.com/)
But this method has one fault about posting on facebook. Octopress doesn't include ogp properties as default. Ogp properties privide facebook meta information such as title, author, description and url. So without this meta information, you cannot get proper images when you write a post on facebook. In order to attach thumbtail image to your post, you have to write some configuration on octopress.

<!-- more -->


<div style="text-align:center" markdown="1">
<img src="/images/posts/2014-02-24-octopress-ogp/before.png" />
</div>


## Write appid and locale

Append below configuration in your `_config.yml`

```
facebook_app_id: YOUR_APP_ID
facebook_locale: ja_JP
```

YOUR_APP_ID might be listed on `/source/_include/facebook_like.html` Paste that number.

## Change facebook like action

Edit `/source/_include/facebook_like.html` like below. This modification makes this JavaScript code get app_id and locale from `_config.yml` file.

```
{% if site.facebook_like %}
<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) {return;}
  js = d.createElement(s); js.id = id; js.async = true;
  js.src = "//connect.facebook.net/{{ site.facebook_locale }}/all.js#appId={{ site.facebook_app_id }}&xfbml=1";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>
{% endif %}
```

## Add top page flag

To ditinguish post articles and top page, add this flag to `source/index.html`

```
---
layout: default
index: true  
---
```

## Configuration for ogp meta informations

Write below meta tags to `source/_includes/custom/facebook_ogp.html`

```
% cat source/_includes/custom/facebook_ogp.html
<meta property="og:title" content="{{ page.title }} - {{ site.title }}" >
<meta property="og:description" content="{{ description | strip_html | condense_spaces | truncate:150 }}" />
<meta property="og:url" content="http://lewuathe.com" />
<meta property="og:image" content="{{ site.url }}{{ site.default_ogp_image }}" />
<meta property="og:author" content="lewuathe" />
<meta property="og:site_name" content="{{ site.title }}" />
<meta property="og:locale" content="{{ site.facebook_locale }}" />
<meta property="og:type" content="{% if page.index %}blog{% else %}article{% endif %}" />
<meta property="fb:app_id" content="{{ site.facebook_app_id }}" />
```

## Include meta tags

At last, make header include these meta tags. Write below on `source/_include/head.html`


<img src="/images/posts/2014-02-24-octopress-ogp/code.png" />

So that's all. It's ok. Deploy this site and post any entry to facebook.


<div style="text-align:center" markdown="1">
<img src="/images/posts/2014-02-24-octopress-ogp/after.png" />
</div>

Good, you can see your thumbnail. A research shows that the post that has thumbnail images attracts more people than 
the post that has no image can. If you are using octopress for writing your own blog, it must be the good option for increasing
the access from facebook. 

Thank you.



