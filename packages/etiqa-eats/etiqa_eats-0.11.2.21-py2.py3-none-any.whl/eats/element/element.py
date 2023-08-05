import base64
import logging
import math
import re
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from pytractor.mixins import WebDriverMixin
from eats.common.exceptions import SearchByElementError, ElementClassError, MultipleWebElementsFoundError
from eats.common.composite_element import CompositeElement


class Element(CompositeElement):
    """Represent a Generic Element on the page"""

    POLL_PERIOD_MILLISEC = 100.0

    _element_type = "element"

    _supported_searches = {
        'xpath': 'find_elements_by_xpath',
        #'binding': 'find_elements_by_binding',
        'exact_binding': 'find_elements_by_exact_binding',
        'model': 'find_elements_by_model'
    }

    def __init__(self, driver, path, search_by='xpath', display_timeout_milliseconds=0, animation_timeout_milliseconds=0):
        self.driver = driver
        self.path = path
        self.search_by = search_by
        self.logger = logging.getLogger("Element")
        self._display_timeout_milliseconds = display_timeout_milliseconds
        self._animation_timeout_milliseconds = animation_timeout_milliseconds

        super(Element, self).__init__()

    def _instantiate_element_from_list(self, *args):
        raise NotImplementedError

    def _instantiate_element(self, element):
        element_obj = super(Element, self)._instantiate_element(element)
        if not isinstance(element_obj, Element):
            raise ElementClassError(type(element_obj))
        return element_obj

    @property
    def web_element(self):
        try:
            find_method_name = self._supported_searches[self.search_by]
            find_ = getattr(self.driver, find_method_name)
        except (KeyError, AttributeError):
            raise SearchByElementError

        found_elements = find_(self.path)
        if not found_elements:
            raise NoSuchElementException(self._find_error_message())
        elif len(found_elements) > 1:
            raise MultipleWebElementsFoundError(self._find_error_message())
        else:
            return found_elements[0]

    def _find_error_message(self):
        return '%s: %s' % (self.search_by, self.path)

    @property
    def element_type(self):
        return self._element_type

    def is_present(self):
        try:
            self.web_element
        except NoSuchElementException:
            return False
        else:
            return True

    def _is_displayed(self):
        try:
            return self.web_element.is_displayed()
        except NoSuchElementException:
            return False
        except StaleElementReferenceException:
            return False

    def is_displayed(self, timeout_milliseconds=None, wait_for_animation=False):
        if timeout_milliseconds is None:
            timeout_milliseconds = self._display_timeout_milliseconds

        if wait_for_animation:
            time.sleep(self._animation_timeout_milliseconds / 1000.0)

        displayed = self._is_displayed()

        wait_iterations = int(math.floor(timeout_milliseconds / self.POLL_PERIOD_MILLISEC))
        poll_period_sec = self.POLL_PERIOD_MILLISEC / 1000.0
        while (not displayed) and (wait_iterations > 0):
            wait_iterations -= 1
            time.sleep(poll_period_sec)
            # in a Selenium Grid environment self._is_displayed() duration
            # has a significant impact that needs to be taken into account
            start = datetime.now()
            displayed = self._is_displayed()
            end = datetime.now()
            duration_millisec = (end - start).total_seconds() * 1000
            correction = int(math.floor(duration_millisec / self.POLL_PERIOD_MILLISEC))
            if correction > 0:
                wait_iterations -= correction

        return displayed

    """Move the focus to the element"""
    def move_to_element(self):
        to_perform = ActionChains(self.driver).move_to_element(self.web_element)
        to_perform.perform()

    def value_of_css_property(self, property_name):
        return self.web_element.value_of_css_property(property_name)

    def double_click(self):
        actions = ActionChains(self.driver)
        actions.double_click(self.web_element)
        actions.perform()

    def is_disabled(self):
        return not self.is_enabled()

    def __getattr__(self, name):
        return getattr(self.web_element, name)

    def get_screenshot(self, file_path):
        base64_encoded_data = self.web_element.screenshot_as_base64()
        binary_data = base64.b64decode(base64_encoded_data)
        with open(file_path, "wb") as fh:
            fh.write(binary_data)

    def click(self):
        try:
            self.web_element.click()
        except WebDriverException as e:
            if re.search(r'Element.* is not clickable at point \(.*, .*\)\. Other element would receive the click', e.msg):
                self.driver.execute_script("arguments[0].scrollIntoView(false);", self.web_element)
                try:
                    self.web_element.click()
                except WebDriverException as e2:
                    if re.search(r'Element.* is not clickable at point \(.*, .*\)\. Other element would receive the click', e2.msg):
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.web_element)
                        self.web_element.click()
                    else:
                        raise
            else:
                raise
