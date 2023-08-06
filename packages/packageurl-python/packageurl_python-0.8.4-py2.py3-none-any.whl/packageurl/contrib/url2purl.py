# -*- coding: utf-8 -*-
#
# Copyright (c) the purl authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Visit https://github.com/package-url/packageurl-python for support and
# download.


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

try:
    from urlparse import urlparse  # Python 2
    from urllib import unquote_plus
except ImportError:
    from urllib.parse import urlparse  # Python 3
    from urllib.parse import unquote_plus

from packageurl import PackageURL
from packageurl.contrib.route import Router
from packageurl.contrib.route import NoRouteAvailable


"""
This module helps build a PackageURL from an arbitrary URL. 
This uses the a routing mechanism available in the route.py module.

In order to make it easy to use, it contains all the conversion functions
in this single Python script.
"""


purl_router = Router()


def get_purl(uri):
    """
    Return a PackageURL inferred from the `uri` string or None.
    """
    if uri:
        try:
            return purl_router.process(uri)
        except NoRouteAvailable:
            return


@purl_router.route('https?://registry.npmjs.*/.*',
                   'https?://registry.yarnpkg.com/.*')
def build_npm_url(uri):
    # npm URLs are difficult to disambiguate with regex
    if '/-/' in uri:
        return build_npm_download_purl(uri)
    else:
        return build_npm_api_purl(uri)


def build_npm_api_purl(uri):
    path = unquote_plus(urlparse(uri).path)
    segments = [seg for seg in path.split('/') if seg]

    if len(segments) != 2:
        return

    # /@invisionag/eslint-config-ivx
    if segments[0].startswith('@'):
        namespace = segments[0]
        name = segments[1]
        return PackageURL('npm', namespace, name)

    # /angular/1.6.6
    else:
        name = segments[0]
        version = segments[1]
        return PackageURL('npm', name=name, version=version)


def build_npm_download_purl(uri):
    path = unquote_plus(urlparse(uri).path)
    segments = [seg for seg in path.split('/') if seg and seg != '-']
    len_segments = len(segments)

    # /@invisionag/eslint-config-ivx/-/eslint-config-ivx-0.0.2.tgz
    if len_segments == 3:
        namespace, name, filename = segments

    # /automatta/-/automatta-0.0.1.tgz
    elif len_segments == 2:
        namespace = None
        name, filename = segments

    else:
        return

    base_filename, ext = os.path.splitext(filename)
    version = base_filename.split('-')[-1]

    return PackageURL('npm', namespace, name, version)


@purl_router.route('https?://repo1.maven.org/maven2/.*',
                   'https?://central.maven.org/maven2/.*',
                   'maven-index://repo1.maven.org/.*')
def build_maven_purl(uri):
    path = unquote_plus(urlparse(uri).path)
    segments = [seg for seg in path.split('/') if seg and seg != 'maven2']

    if len(segments) < 3:
        return

    before_last_segment, last_segment = segments[-2:]
    has_filename = before_last_segment in last_segment

    filename = None
    if has_filename:
        filename = segments.pop()

    version = segments[-1]
    name = segments[-2]
    namespace = '.'.join(segments[:-2])
    qualifiers = {}

    if filename:
        name_version = '{}-{}'.format(name, version)
        _, _, classifier_ext = filename.rpartition(name_version)
        classifier, _, extension = classifier_ext.partition('.')
        if not extension:
            return

        qualifiers['classifier'] = classifier.strip('-')

        valid_types = ('aar', 'ear', 'mar', 'pom', 'rar', 'rpm',
                       'sar', 'tar.gz', 'war', 'zip')
        if extension in valid_types:
            qualifiers['type'] = extension

    return PackageURL('maven', namespace, name, version, qualifiers)


@purl_router.route('https?://rubygems.org/downloads/.*')
def build_rubygems_url(uri):
    if uri.endswith('/') or not uri.endswith('.gem'):
        return

    path = unquote_plus(urlparse(uri).path)
    last_segment = path.split('/')[-1]
    archive_basename = last_segment.rstrip('.gem')
    name, _, version = archive_basename.rpartition('-')

    return PackageURL('rubygems', name=name, version=version)
