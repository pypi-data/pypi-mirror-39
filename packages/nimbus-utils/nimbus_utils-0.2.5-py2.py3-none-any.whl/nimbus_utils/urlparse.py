# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
import six

if six.PY3:
    from urllib.parse import urlparse, urljoin, parse_qs, parse_qsl
else:
    from urlparse import urlparse, urljoin, parse_qs, parse_qsl

__all__ = [
    "urlparse",
    "urljoin",
    "parse_qs",
    "parse_qsl",
]
