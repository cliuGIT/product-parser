#!/usr/bin/env python
__author__ = 'cliu'


import re
import sys
import urllib2
import socket
import traceback
import gzip
from StringIO import StringIO
from functools import wraps

import parsers
from loggers import create_simple_logger

logger = create_simple_logger('ProductParser')

domain_regex = re.compile(r'^https?://(?P<domain>[a-zA-Z0-9\.]+)')

domain_mapper = [
    ('product.dangdang.com', parsers.dangdang),
    ('item.yhd.com', parsers.yihao),
]


class Fetcher:
    """
    obj = Fetcher()
    status, content = obj.fetch_url(url)

    status      True | False
    content     html | error msg
    """
    def __init__(self):
        self._http_data = None
        self._http_headers = {'Accept-Encoding': 'gzip'}
        self._timeout = 10

    def fetch_url(self, url):
        msg = ''
        req = urllib2.Request(url, self._http_data, self._http_headers)
        try:
            response = urllib2.urlopen(req, timeout=self._timeout)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                content = f.read()
            else:
                content = response.read()
            return True, content

        except urllib2.HTTPError, e:
            msg = e.code
        except urllib2.URLError, e:
            msg = 'urllib2.URLError: {0}'.format(e)
        except socket.timeout:
            msg = 'socket.timeout'
        except ValueError, e:
            msg = e
        except KeyboardInterrupt:
            sys.exit(1)
        except SystemExit:
            sys.exit(1)
        except Exception, e:
            msg = 'Unknown exception: {0}\n{1}'.format(e, traceback.format_exc())
        return False, msg

    def set_timeout(self, seconds):
        self._timeout = seconds

    def set_http_data(self, data=None):
        self._http_data = data

    def set_http_headers(self, headers=None):
        self._http_headers = headers

    def set_browser(self):
        """
        under developing
        """
        pass


def _parse_domain(url):
    r = domain_regex.search(url)
    if r:
        return r.group('domain')
    return ''


def _get_parser(raw_domain):
    if raw_domain:
        for d, Parser in domain_mapper:
            if raw_domain.endswith(d):
                return Parser


def fetcher_wrapper(f):
    @wraps(f)
    def wrapped_function(url):
        status, msg = f(url)
        if status:
            logger.info('Fetched\t%s', url)
            try:
                msg = msg.decode('gb18030').encode('utf8')
            except:
                pass
        else:
            logger.warning('%s\t%s', msg, url)
        return status, msg
    return wrapped_function


def get(url):
    """main function"""
    title, price, srcs = '', '', []
    logger.debug('Given\t%s', url)
    if not url.startswith('http'):
        url = 'http://%s' % url

    domain = _parse_domain(url)
    f = Fetcher()
    f.set_timeout(3)
    parser = _get_parser(domain)
    if parser:
        title, price, srcs = parser(url, fetcher_wrapper(f.fetch_url))
        title = title.replace('&nbsp;', '').strip()
        if not (title and price and srcs):
            logger.error('Parse error: %s', url)
    return title, price, srcs


def usage():
    print """
    Product Parser single url test.

    Usage:
    ./test.py http://www.blabla.com/blablablabla
"""


def ensure_console(s):
    if sys.platform == 'win32' and isinstance(s, str):
        return s.decode('utf8').encode('gbk')
    return s


if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[-1]
        title, price, srcs = get(url)
        logger.info(ensure_console(title))
        logger.info(price)
        for src in srcs:
            logger.info(src)
    else:
        usage()
