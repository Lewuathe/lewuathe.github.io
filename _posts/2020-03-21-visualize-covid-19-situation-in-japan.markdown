---
title: "Visualize COVID-19 situation in Japan"
layout: post
date: 2020-03-21 22:00:40 +0900
image: 'assets/img/posts/2020-03-21-visualize-covid-19-situation-in-japan/catch.png'
description:
tag: ['COVID-19', 'TypeScript', 'Data']
blog: true
author: "Kai Sasaki"
---

Visualization often provides us a vivid image to grasp the situation at a glance. It is one of the recommended ways as a starting point of more in-depth understanding and investigation in general.

COVID-19 keeps spreading all around the world. The number of infectious cases is growing, especially in Europe. That challenge will keep going on for a while. The prolonged war reminds us of the criticalness to get the correct information consistently, and visualization will play a significant role in helping various kinds of effort. For instance, many visualization works are happening to help people understand the situation and deal with this challenge as follows.

- [Coronavirus Disease (COVID-19) Situation Report in Japan](https://toyokeizai.net/sp/visual/tko/covid19/en.html)
- [Latest updates on COVID-19 in Tokyo](https://stopcovid19.metro.tokyo.lg.jp/)

As a part of this type of effort, I have created another tool to provide statistical information related to the COVID-19 situation in Japan. It includes the aggregated statistics relating to the medical system in Japan supporting COVID-19 remediation.

# What is Choropleth

A [choropleth](https://en.wikipedia.org/wiki/Choropleth_map) map is a type of map in which areas are shaded in proportion to statistical measurement. The map is useful to see aggregated information by the area segmented on the map quickly.

The tool used a choropleth map to illustrate the statistical measurement at a glance. Here is the illustration provided by the tool.

- **[https://www.lewuathe.com/choropleth/](https://www.lewuathe.com/choropleth/)**

[![preview](/assets/img/posts/2020-03-21-visualize-covid-19-situation-in-japan/preview.png)](https://www.lewuathe.com/choropleth/)

The data was obtained from the following sites.

- [Toyo Keizai](https://toyokeizai.net/sp/visual/tko/covid19/en.html)
- [Japan Cabinet Office](https://www5.cao.go.jp/keizai-shimon/kaigi/special/reform/mieruka/data/p2/index.html)

Regarding the statistics from the census, it uses the data in 2013, which seems to have higher coverage in terms of medical and health care attributes.

# Supported Data

Currently, the following data is supported.

- Total population
- Total confirmed cases of COVID-19
- The ratio of confirmed cases to the population
- The ratio of hospitals to the confirmed cases
- The number of hospitals
- The number of beds per 100,000 people
- The number of doctors per 100,000 people

I will continue to extend the data set to show the COVID-19 situation from various kinds of perspective.

# Acknowledgement

The original tool created by [ncovis](https://github.com/ncovis) designed to visualize the situation in China profoundly inspired my visualization. The design and appearance of the [ncovis/choropleth](https://ncovis.github.io/choropleth/) were so impressive to me that I decided to make use of it. I appreciate the ncovis' work. 