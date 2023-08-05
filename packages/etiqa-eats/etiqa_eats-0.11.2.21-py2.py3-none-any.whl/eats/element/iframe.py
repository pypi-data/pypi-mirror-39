import six
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from eats.element import Element


class Iframe(Element):

    _element_type = 'iframe'

    def __init__(self, *args, **kwargs):
        super(Iframe, self).__init__(*args, **kwargs)

    def enter(self):
        self.driver.switch_to.frame(self.web_element)

    def exit(self):
        self.driver.switch_to.default_content()


class VisibleReCaptcha(Iframe):

    def __init__(self, *args, **kwargs):
        super(VisibleReCaptcha, self).__init__(*args, **kwargs)

    _element_type = 'recaptcha'

    def _load_elements(self):
        self.add_element('recaptcha_checkbox', VisibleReCaptchaChecbox(self.driver, "//span[@id='recaptcha-anchor']"))
        self.add_element('recaptcha_checkmark', Element(self.driver, "//span[@aria-disabled='false']", display_timeout_milliseconds=5000))
        self.add_element('testing_recaptcha_alert', IframeElement(self, self.driver, "//div[@class='rc-anchor-alert']", display_timeout_milliseconds=5000))

    def check(self):
        self.enter()
        try:
            self.get_element('recaptcha_checkbox').click_checkbox()
            wait = WebDriverWait(self.driver, 10)
            check_mark = self.get_element('recaptcha_checkmark')
            check_mark = wait.until(EC.visibility_of_element_located((By.XPATH, check_mark.path)))
            checked_checkbox = Element(self.driver, "//span[@role='checkbox' and @aria-checked='true']")
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, checked_checkbox.path)))
        finally:
            self.exit()

    def set_value(self, value):
        if self._bool(value) == (not self.is_checked()):
            self.check()

    def _bool(self, value):
        if type(value) is bool:
            return value
        else:
            value = six.text_type(value).lower()
            return value in {'true', 'yes', '1', 'checked'}

    def is_checked(self):
        self.enter()
        try:
            return self._bool(self.get_element('recaptcha_checkbox').get_attribute('aria-checked'))
        finally:
            self.exit()

    def get_value(self):
        return self.is_checked()

    def is_testing_captcha(self):
        self.enter()
        try:
            return self.get_element('testing_recaptcha_alert')
        finally:
            self.exit()


class VisibleReCaptchaChecbox(Element):

    def click_checkbox(self):
        self.driver.execute_script("document.getElementById('recaptcha-anchor').click();")


class IframeElement(Element):

    def __init__(self, iframe, *args, **kwargs):
        super(IframeElement, self).__init__(*args, **kwargs)
        self.iframe = iframe

    def is_displayed(self):
        self.iframe.enter()
        try:
            return super(IframeElement, self).is_displayed()
        finally:
            self.iframe.exit()
