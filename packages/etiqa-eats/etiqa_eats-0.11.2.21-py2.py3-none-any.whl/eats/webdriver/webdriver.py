import six
if six.PY2:
    from urllib import unquote
else:
    from urllib.parse import unquote
from pkg_resources import resource_string
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, RemoteDriverServerException
from eats.utils.window import Window
from selenium.webdriver.remote.webdriver import WebDriver as __SeleniumWebDriver
from pytractor.webdriver import Remote as __PytractorWebDriver, WebDriverMixin
from appium.webdriver import Remote as __AppiumWebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import json
import re
EATS_SCRIPTS_DIR = 'scripts'


class EatsWebDriver(object):

    def __init__(self, *args, **kwargs):
        super(EatsWebDriver, self).__init__(*args, **kwargs)
        self._window = Window(self)

    @property
    def window(self):
        return self._window

    def current_url_unquote(self, encoding='utf-8'):
        if six.PY2:
            cu = self.current_url.encode(encoding)
            return unquote(cu).decode(encoding)
        else:
            return unquote(self.current_url, encoding)

    def find_elements_by_css_property(self, attribute, value, using=None):
        elements = self._eats_execute_client_script('findByCssProperty', attribute, value, using, async=False)
        return elements

    def find_element_by_css_property(self, attribute, value, using=None):
        elements = self.find_elements_by_css_property(attribute, value, using=using)
        if len(elements) == 0:
            raise NoSuchElementException(
                "No element found for css property"
                " '{}' with value '{}'".format(attribute, value)
            )
        else:
            return elements[0]

    def find_elements_with_fixed_position(self):
        elements = self.find_elements_by_css_property("position", "fixed")
        visible_elements = [element for element in elements if element.is_displayed()]
        return visible_elements

    def get_element_coordinate(self, element, using=None):
        return json.loads(self._eats_execute_client_script('ElementCoordinates', element, using, async=False))

    def get_metadata_elements_content(self):
        elements = self.find_elements_by_xpath("//meta")
        contents = []
        for element in elements:
            try:
                name = element.get_attribute("name")
                content = element.get_attribute("content")
                contents.append({"name": name, "content": content})
            except NoSuchAttributeException:
                pass
        return contents

    def get_metadata_elements_content_by_name(self, name):
        elements = self.find_elements_by_xpath("//meta[@name='" + name + "']")
        contents = []
        for element in elements:
            try:
                content = element.get_attribute("content")
            except NoSuchAttributeException:
                content = ""
            contents.append({"content": content})
        return contents

    def get_element_shadow(self, element):
        coords = self.get_element_coordinate(element, using=None)
        if coords["shadow"] != "none":
            _SHADOW = r'(-{0,1}[0-9]+)px (-{0,1}[0-9]+)px (-{0,1}[0-9]+)px (-{0,1}[0-9]+)px'
            values = re.search(_SHADOW, coords["shadow"]).groups()
            return {
                'offset-x': int(values[0]),
                'offset-y': int(values[1]),
                'blur-radius': int(values[2]),
                'spread-radius': int(values[3]),
                'height': abs(int(values[1])) + int(values[2]) + int(values[3])
            }
        else:
            return {
                'offset-x': 0,
                'offset-y': 0,
                'blur-radius': 0,
                'spread-radius': 0
            }

    def get_element_computed_style(self, element, attribute, using=None):
        return self._eats_execute_client_script('GetComputedStyle', element, attribute, using, async=False)

    def get_google_tracking_keys(self):
            return json.loads(self._eats_execute_client_script('GetGoogleTrackingKeys', async=False))

    def get_platform_name(self):
        if "platformName" in self.desired_capabilities:
            return self.desired_capabilities["platformName"]
        elif "platform" in self.desired_capabilities:
            return self.desired_capabilities["platform"]
        else:
            return ""

    def get_device_name(self):
        if "deviceName" in self.desired_capabilities:
            return self.desired_capabilities["deviceName"]
        else:
            return "Desktop"

    def get_browser_name(self):
        if "browserName" in self.desired_capabilities:
            return self.desired_capabilities["browserName"]
        else:
            return "Unknown"

    def send_special_key(self, key):
        if hasattr(Keys, key):
            to_perform = ActionChains(self.driver).send_keys(getattr(Keys, key))
            to_perform.perform()
        else:
            raise RemoteDriverServerException("{unsupported_key} is not supported".format(unsupported_key=key))

    def _eats_execute_client_script(self, script_name, *args, **kwargs):
        async = kwargs.pop('async', True)
        file_name = '{}.js'.format(script_name)
        js_script = resource_string(__name__,
                                    '{}/{}'.format(EATS_SCRIPTS_DIR,
                                                   file_name))
        if js_script:
            js_script = js_script.decode('UTF-8')
        if async:
            result = self.execute_async_script(js_script, *args)
        else:
            result = self.execute_script(js_script, *args)
        return result


class SeleniumWebDriver(EatsWebDriver, __SeleniumWebDriver):
    pass


class PytractorWebDriver(EatsWebDriver, __PytractorWebDriver):
    pass


class AngularFirefoxWebDriver(SeleniumWebDriver):

    def wait_for_angular(self):
        pass


class AppiumWebDriver(EatsWebDriver, __AppiumWebDriver):
    pass


class PytractorAppiumWebDriver(EatsWebDriver, WebDriverMixin, __AppiumWebDriver):
    pass


def web_driver_factory(context, angular=False):
    extra_params = {}

    browser_name = context.config.userdata.get('browser', 'chrome')

    if angular:
        appium_driver = AppiumWebDriver
        if browser_name.lower() in ['internetexplorer']:
            webdriver_driver = AngularFirefoxWebDriver
        else:
            webdriver_driver = PytractorWebDriver
            extra_params['test_timeout'] = 20000
    else:
        appium_driver = AppiumWebDriver
        webdriver_driver = SeleniumWebDriver

    desired_capabilities = getattr(DesiredCapabilities, browser_name.upper())

    if context.config.userdata.get('platform_name', 'ANY') == 'iOS':
        desired_capabilities.update({
            'platformVersion': context.config.userdata.get('platform_version', 'ANY'),
            'deviceName': context.config.userdata.get('device_name', 'ANY'),
            'platformName': context.config.userdata.get('platform_name', 'ANY'),
            'automationName': 'XCUITest',
            'orientation': context.config.userdata.get('orientation', 'PORTRAIT'),
            'platform': context.config.userdata.get('platform', 'ANY')
        })
        driver_class = appium_driver
        extra_params = {}
    else:
        driver_class = webdriver_driver

    driver = driver_class(
        command_executor=context.config.userdata.get('command_executor','http://127.0.0.1:4444/wd/hub'),
        desired_capabilities=desired_capabilities,
        **extra_params
    )
    driver.set_script_timeout(120)
    if context.config.userdata.get('platform_name', 'ANY') != 'iOS' and context.config.userdata.get('platform_name', 'ANY') != 'Android':
        driver.maximize_window()
    return driver
