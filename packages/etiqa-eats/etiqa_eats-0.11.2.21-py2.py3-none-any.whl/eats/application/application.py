__author__ = 'pulphix'

import six

if six.PY2:
    from urlparse import urljoin, urlparse
else:
    from urllib.parse import urljoin, urlparse
import base64
from eats.common.exceptions import ElementNotFoundError, PageNotFoundError, PageNameIsNoneError
from eats.common.composite_element import CompositeElement
from eats.common.utils import is_absolute_url
from selenium.webdriver.support.ui import WebDriverWait


class Application(CompositeElement):
    def __init__(self, driver, base_url=None):
        self.__current_page = None
        self.driver = driver
        self.base_url = base_url
        super(Application, self).__init__()

    @property
    def current_page(self):
        return self.__current_page

    @current_page.setter
    def current_page(self, page):
        assert page.name in self._elements
        self.__current_page = page

    @property
    def prod_netloc(self):
        url = urlparse(self.base_url)
        return url.netloc

    @property
    def prod_http_base_url(self):
        return "http://" + self.prod_netloc

    @property
    def prod_https_base_url(self):
        return "https://" + self.prod_netloc

    def get_page(self, name):
        try:
            return self.get_element(name)
        except ElementNotFoundError:
            raise PageNotFoundError(name)

    def add_page(self, page):
        if page.name is not None:
            self.add_element(page.name, page)
        else:
            raise PageNameIsNoneError

    def go_to_url(self, url):
        if not is_absolute_url(url):
            url = urljoin(self.base_url, url)
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url_unquote()

    def get_screenshot(self, file_path):
        base64_encoded = self.driver.get_screenshot_as_base64()
        decoded_bytes = base64.b64decode(base64_encoded)
        with open(file_path, "wb") as fh:
            fh.write(decoded_bytes)

    def get_platform_name(self):
        if "platformName" in self.driver.desired_capabilities:
            return self.driver.desired_capabilities["platformName"]
        else:
            return ""

    """Get page source"""

    def get_page_source(self):
        html_doc = self.driver.page_source
        return html_doc

    def _add_sub_elements(self, element):
        pass
