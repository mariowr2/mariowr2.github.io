# SETUP
1. `$ sudo apt-get install ruby-full build-essential zlib1g-dev`

2. 
```
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

3. `$ gem install jekyll bundler`

4. `$ gem install jekyll jekyll-paginate jemoji html-proofer`


# { Personal } Jekyll Theme
![Build Status](https://travis-ci.org/le4ker/personal-jekyll-theme.svg?branch=master)
![license](https://img.shields.io/badge/license-MIT-blue.svg?link=https://github.com/dono-app/ios/blob/master/LICENSE)
[![Join the chat at https://gitter.im/PanosSakkos/personal-jekyll-theme](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/panossakkos/personal-jekyll-theme?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

{ Personal } is a free responsive Jekyll theme, about you :wink:

You can watch it in action [here](https://le4ker.github.io/personal-jekyll-theme/)!

<img src="https://github.com/le4ker/personal-jekyll-theme/raw/master/.github/personal-mobile.mov.gif" height="480">

<img src="https://github.com/le4ker/personal-jekyll-theme/raw/master/.github/personal-desktop.mov.gif" height="600" width="960">

## What value does { Personal } add

* Fork of [Timeline](https://github.com/kirbyt/timeline-jekyll-theme) (mashup of [Grayscale by Start Bootstrap](https://github.com/IronSummitMedia/startbootstrap-grayscale) and [Agency Jekyll Theme](https://github.com/y7kim/agency-jekyll-theme))
  * Modern and minimal design
    * Responsive templates for home page, blog archive and posts. Looks great on mobile, tablet, and desktop devices
    * Sweet animations
    * Gracefully degrades in older browsers. Compatible with Internet Explorer 8+ and all modern browsers
  * Timeline
    * Tell your story so far with a sleek timeline of dates, pictures and descriptions
  * White on black text, making the reading experience tireless
  * Google analytics  
* Customization and full control of your website and blog through the site config
* Customization of the website's coloring
* Blogging functionality
  * Preview of the latest post in the home page
  * Archive page
  * Syntax highlighting
  * Emojis
  * Gesture navigation in archive and post pages by swiping
  * Hashtags
  * Categories
  * Disqus comments
  * Bootstrap share buttons
  * RSS feed
* Author blurb under the posts
* 404 page
* iOS and Android Web App mode
* Enforcing of https protocol
* Protection from email harvesting
* Sitemap
* Travis CI integration with [html-proofer](https://github.com/gjtorikian/html-proofer)

## Documentation

The theme contains documentation in the form of [blog posts](https://le4ker.github.io/personal-jekyll-theme/blog/index.html).

## How to run locally

First, you need to install jekyll and the dependencies of { Personal } by running:

```shell
./scripts/install
```

Then, you can build and serve your website by simply running:

```shell
./scripts/serve-production
```

To serve across lan (requires su to forward the port 4000 over lan):

```shell
./scripts/serve-lan-production
```
