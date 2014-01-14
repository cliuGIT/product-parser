__author__ = 'cliu'


import re

import parsers

domain_regex = re.compile(r'^(https?://)?(?P<domain>[a-zA-Z0-9\.]+)')

domain_mapper = [
    ('dangdang.com', parsers.Dangdang),
]


def _parse_domain(url):
    r = domain_regex.search(url)
    if r:
        return r.group('domain')
    return None


def _get_parser(raw_domain):
    for d, Parser in domain_mapper:
        if raw_domain.endswith(d):
            return Parser


def get(url):
    domain = _parse_domain(url)
    Parser = _get_parser(domain)
    p = Parser(url)
