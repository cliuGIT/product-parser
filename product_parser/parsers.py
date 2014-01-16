import re
import logging


logger = logging.getLogger('ProductParser')

__author__ = 'cliu'


rg_price = re.compile(r'(\d+\.?\d+)')
rg_tag = re.compile(r'<.+?>')


def _parse_price(html):
    r = rg_price.search(html)
    if r:
        return r.group(1)
    return ''


def _parse_html_tag(html, tag_name, keyword):
    r = re.search(r'<%s[^>]*%s[^>]*>.*?</%s>' % (tag_name, keyword, tag_name), html, flags=re.M | re.S)
    if r:
        return r.group(0)
    return ''


def _parse_html_single_tag(html, tag_name, keyword):
    r = re.search(r'<%s[^>]*%s[^>]*>' % (tag_name, keyword), html, flags=re.M | re.S)
    if r:
        return r.group(0)
    return ''


def _parse_html_attrs(html, tag_name, attr):
    return re.findall(r'<%s[^>]+%s=[\'"](.+?)[\'"]' % (tag_name, attr), html, flags=re.M | re.S)


def _parse_html_single_attr(html, attr):
    r = re.search(r'%s=[\'"](.+?)[\'"]' % attr, html, flags=re.M | re.S)
    if r:
        return r.group(1)
    return ''


def _get_html_price(html, tag_name, keyword):
    r = _parse_html_tag(html, tag_name, keyword)
    if r:
        return _parse_price(r)
    return ''


def _get_html_attrs(html, outer_tag_name, outer_tag_keyword, inner_tag_name, inner_attr_name):
    outer_tag_html = _parse_html_tag(html, outer_tag_name, outer_tag_keyword)
    if outer_tag_html:
        return _parse_html_attrs(outer_tag_html, inner_tag_name, inner_attr_name)
    return []


def _get_html_single_attr(html, outer_tag_name, outer_tag_keyword, inner_attr_name):
    outer_tag_html = _parse_html_single_tag(html, outer_tag_name, outer_tag_keyword)
    if outer_tag_html:
        return _parse_html_single_attr(outer_tag_html, inner_attr_name)
    return ''


def _get_html_title(html, tag_name, keyword):
    r = _parse_html_tag(html, tag_name, keyword)
    if r:
        return rg_tag.sub('', r)
    return ''


rg_yihao_main = re.compile(r'/item/(\d+)')
rg_yihao_promo = re.compile(r'/item/lp/\d+_(\d+)_\d+')
def yihao(url, fetcher):
    title, price, srcs = '', '', []
    r = rg_yihao_promo.search(url)
    if r:
        url = 'http://item.yhd.com/item/%s' % r.group(1)

    status, html = fetcher(url)
    if status:
        title = _get_html_title(html, 'h1', 'productMainName')
        price = _get_html_price(html, 'span', 'current_price')
        srcs = [src.replace('60x60', '450x450') for src in _get_html_attrs(html, 'ul', 'imgtab_con', 'img', 'src')]

    return title, price, srcs


rg_dang_main = re.compile(r'/(\d+).html')
def dangdang(url, fetcher):
    title, price, srcs = '', '', []
    r = rg_dang_main.search(url)
    if r:
        url = 'http://product.dangdang.com/%s.html' % r.group(1)
        status, html = fetcher(url)
        if status:
            title = _get_html_title(_parse_html_tag(html, 'div', 'Title_pub'), 'h1', '')
            price = _get_html_price(html, 'b', 'd_price')
            srcs = _get_html_attrs(html, 'ul', 'pic_list', 'a', 'id')
    return title, price, srcs

