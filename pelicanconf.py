#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Henk'
SITENAME = '~/hgrif'
SITEURL = ''

THEME='/Users/henkgriffioen/projects/pelican-themes/pelican-simplegrey/'

PATH = 'content'

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

STATIC_PATHS = ['images']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['./plugins']
#PLUGINS = ["latex"]
PLUGINS = ['render_math']
#PLUGINS = ["pelican.plugins.latex"]

# Only use LaTeX for selected articles

#LATEX = 'article'
