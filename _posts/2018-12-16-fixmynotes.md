---
layout: post
section-type: post
title: fixmynotes.com, make studying easier!
category: Projects
tags: [ 'python', 'openCV',"flask" ]
---
When studying for my courses, I found myself performing the same task over and over: Opening slides,and zooming
on each in order to be able to read it. This became tiring very quickly, and I wondered if there was anything I could do about it (besides creating a change.org for profs to change their slides), and so this idea became my first 'solo' project.  

For clarification, my intent was to transform a set of slides that looked like this:
<div style="text-align: center">
    <img  src="{{site.baseurl}}{{ site.slides }}" alt="">
</div>
<br/>
Into a document where each of these slides would get its own page. For this project I used the Flask framework on top of Nginx inside an Ubuntu virtual machine. The user uploads the document containing the slides he wishes to "fix" . Flask passes the document to a python script which uses OpenCV (A computer vision library) to find the slides, and after finding them, uses the Python image library and other libraries for creating PDF files to carry out the job. The whole process looks like this:

<div style="text-align: center">
    <img  src="{{site.baseurl}}{{ site.project_demo }}" alt="">
</div>
<br/>

Doing this project was a very challenging and rewarding experience! The source code and setup instructions can be found [here](https://github.com/mariowr2/fixmynotes.com). Pull requests are welcome!
