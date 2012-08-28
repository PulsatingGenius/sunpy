# -*- coding: utf-8 -*-
# Author: Florian Mayer <florian.mayer@bitsrc.org>

from __future__ import absolute_import

import os
import re
import sys

# For Content-Disposition parsing
from email.parser import FeedParser
from unicodedata import normalize
from itertools import ifilter

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'_', encoding="ascii"):
    if isinstance(text, unicode):
        text = normalize('NFKD', text)
    return unicode(delim).join(ifilter(None, (
        word.encode(encoding, 'ignore')
        for word in _punct_re.split(text.lower())        
        )))


def get_content_disposition(content_disposition):
    parser = FeedParser()
    parser.feed('Content-Disposition: ' + content_disposition)
    name = parser.close().get_filename()
    if not isinstance(name, unicode):
        name = name.decode('latin1', 'ignore')
    return name


def get_filename(sock, url):
    name = None
    cd = sock.headers.get('Content-Disposition', None)
    if cd is not None:
        try:
            name = get_content_disposition(cd)
        except IndexError:
            pass

    if not name:
        no_get = url.rsplit('?', 1)[0]
        name = no_get.rstrip('/').rsplit("/", 1)[-1]
    return unicode(name)


def get_system_filename(sock, url, default=u"file"):
    name = get_filename(sock, url)
    if not name:
        name = unicode(default)
    return name.encode(sys.getfilesystemencoding())
