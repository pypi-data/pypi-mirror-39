import six
if six.PY2:
    from urlparse import urlparse, urldefrag
else:
    from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup
from eats.element import Element
from eats.common.composite_element import CompositeElement
from eats.common.exceptions import ElementNotFoundError, ElementClassError, IAmNotOnPageError
from eats.common import utils
from eats.utils.screenshot import Screenshot


class Page(CompositeElement):
    _name = None
    _driver = None
    _url = None

    def __init__(self, driver, url):
        self._driver = driver
        self._url = url
        super(Page, self).__init__()

    @property
    def name(self):
        return self._name

    @property
    def driver(self):
        return self._driver

    @property
    def url(self):
        return self._url

    @property
    def url_without_fragment(self):
        return urldefrag(self.url)[0]

    def add_element(self, name, element, add_sub_elements=True):
        if not isinstance(element, Element):
            raise ElementClassError
        super(Page, self).add_element(name, element, add_sub_elements)

    """Return Current URL"""
    def current_url(self):
        return self._driver.current_url_unquote()

    """Get page source"""
    def get_page_source(self):
        html_doc = self._driver.page_source
        return html_doc

    """Get metatag content"""
    def get_meta_name_content(self, meta_name):
        html = self.get_page_source()
        soup = BeautifulSoup(html, "html.parser")
        try:
            return soup.find("head").find("meta", {"name": meta_name})['content']
        except TypeError:
            return None

    """Return page title"""
    def get_title(self):
        return self.driver.title

    """Get the info about the favicon, if favicon is not set return the path of the default favicon"""
    def get_favicon_info(self):
        html = self.get_page_source()
        soup = BeautifulSoup(html, "html.parser")
        try:
            return soup.find("head").find("link", {"rel": "icon"})['href']
        except TypeError:
            return None

    def get_favicon_url(self):
        href = self.get_favicon_info()
        if href is None:
            return utils.get_root_url(self.current_url()) + "favicon.ico"
        url_obj = urlparse(href)
        if href.startwith('//'):
            url_obj = urlparse(self.current_url())
            return url_obj.scheme + href
        elif url_obj.scheme == '':
            return utils.get_root_url(self.current_url()) + href

    """Go to Page"""
    def goto(self):
        self._driver.get(self._url)

    def i_am_on_page(self):
        current = self.current_url()
        if current != self._url:
            return False, 'The url is: "%s" instead of "%s"' % (current, self._url)
        return True, 'I am on page %s' % self.name

    def is_loaded(self):
        return False

    def get_full_screenshot(self, filename):
        if hasattr(self._driver, "window"):
            screenshot = Screenshot(self._driver.window)
            screenshot.get_page_screenshot(filename)
        else:
            raise Exception("driver do not support window object")

    def get_screenshot(self, filename):
        if hasattr(self._driver, "window"):
            screenshot = Screenshot(self._driver.window)
            screenshot.get_screenshot(filename)
        else:
            raise Exception("driver do not support window object")