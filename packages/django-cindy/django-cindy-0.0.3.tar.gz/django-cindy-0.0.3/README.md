# Cindy

Cindy is a django app that takes any kind of content syndication channel (RSS, Atom, or
anything that can be parsed by feedparser) and creates a new Atom feed, which actual full-text
versions of the feed entries.

[Boris Spiders](https://bitbucket.org/lullis/django_boris) are used to download and parse the content of the link

Cindy is the original application developed for the [nofollow](https://bitbucket.org/lullis/nofollow)
project and its main use-case for now.
