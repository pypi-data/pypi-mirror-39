# -*- coding: utf-8 -*-
import six
if six.PY2:
    from urlparse import urlparse, urlunparse
    from urllib import quote
else:
    from urllib.parse import urlunparse, urlparse, quote

from bs4 import BeautifulSoup as Soup


def sitemap_parser(contents):
    soup = Soup(contents, "lxml")

    # find all the <url> tags in the document
    urls = soup.findAll('url')

    # no urls? bail
    if not urls:
        return False

    # storage for later...
    out = []

    for u in urls:
        loc = u.find('loc').string
        prio = u.find('priority').string
        change = u.find('changefreq').string
        last = u.find('lastmod').string
        out.append({"loc": loc, "lastmod": last, "priority": prio, "changefreq": change})
    return out


def replace_env_url_to_prod(url, prod_netloc):
    o = urlparse(url)
    return six.text_type(url.replace(o.netloc, prod_netloc))


def url_encode(url, encoding='utf8'):
    o = urlparse(url)
    path = quote(o.path.encode(encoding))
    o = list(o)
    o[2] = path
    return urlunparse(o)


class SiteMapGen(object):
    def __init__(self, pages):
        self._pages = pages

    def write_xml(self, path):
        of = open(path, 'w')
        of.write(u'<?xml version="1.0" encoding="utf-8"?>\n')
        of.write(u'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
        url_str = u'<url><loc>{}</loc><lastmod>{}</lastmod><changefreq>{}</changefreq><priority>{}</priority></url>\n'
        for exp in self._pages:
            of.write(url_str.format(exp["loc"],  exp["lastmod"], exp["changefreq"], exp["priority"]).encode('utf8'))

        of.write(u'</urlset>')
        of.close()
