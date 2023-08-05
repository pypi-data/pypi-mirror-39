from pkg_resources import resource_string

CLIENT_SCRIPTS_DIR = 'scripts'
import json


class Window(object):

    def __init__(self, driver, default_size=None):
        self.driver = driver

        if not default_size:
            self.default_size = 1366, 1024
        else:
            self.default_size = default_size

    def set_default(self, default_size):
        self.default_size = default_size

    def get_width(self):
        return self.driver.get_window_size().get("width")

    def get_height(self):
        return self.driver.get_window_size().get("height")

    def page_height(self):
        return self.page_size()["height"]

    def page_width(self):
        return self.page_size()["width"]

    def page_size(self):
        return json.loads(self._execute_client_script('PageSize', async=False))

    def page_sizes(self):
        size = self.page_size()
        return size["width"], size["height"]

    def page_max_height(self):
        return self._execute_client_script('PageMaxHeight', async=False)

    def page_scroll_height(self):
        return self._execute_client_script('PageScrollHeight', async=False)

    def resize_default(self):
        self.driver.set_window_size(*self.default_size)

    def resize_max_height(self, offset=None):
        if not offset:
            offset = 0
        self.driver.set_window_size(self.get_width(), self.page_max_height() + offset)

    def offset_position(self):
        return self.driver.execute_script("return window.pageYOffset;")

    def scroll_by(self, scroll):
        return self.driver.execute_script("window.scrollBy(" + str(scroll[0]) + "," + str(scroll[1]) + ")");

    def scroll_to(self, position):
        self.driver.execute_script("window.scrollTo(" + str(position[0]) + "," + str(position[1]) + ");")

    def scroll_to_top(self):
        self.scroll_to((0, 0))

    def scroll_to_bottom(self):
        self.scroll_to((0, self.page_max_height()))

    def get_scroll_top(self):
        return self.driver.execute_script("return window.pageYOffset")

    def get_total_scroll(self):
        return self.driver.execute_script("return window.pageYOffset + window.innerHeight")

    def is_bottom_page(self):
        return self.get_total_scroll() == self.page_max_height()

    def is_top_page(self):
        return self.get_scroll_top() == 0

    def is_mobile(self):
        return MobileDevice.is_supported_platform(self.driver.get_platform_name())

    def pixel_ratio(self):
        if self.is_mobile():
            device = self._get_mobile_device()
            return device.pixel_ratio()
        else:
            return 1

    def get_fixed_border(self):
        if self.is_mobile():
            device = self._get_mobile_device()
            return device.get_fixed_border()
        else:
            return {"top": 0, "bottom": 0}

    def get_crops(self):
        if self.is_mobile():
            device = self._get_mobile_device()
            crops = device.get_crops()
            orientation = self.driver.orientation
            return {k: crops[orientation][k] * device.pixel_ratio() for k in crops[orientation]}
        else:
            width, height = self.page_sizes()
            return {"x": 0, "y": 0, "width": width, "height": height}

    def _execute_client_script(self, script_name, *args, **kwargs):
        async = kwargs.pop('async', True)
        file_name = '{}.js'.format(script_name)
        js_script = resource_string(__name__,
                                    '{}/{}'.format(CLIENT_SCRIPTS_DIR,
                                                   file_name))
        if js_script:
            js_script = js_script.decode('UTF-8')
        if async:
            result = self.driver.execute_async_script(js_script, *args)
        else:
            result = self.driver.execute_script(js_script, *args)
        return result

    def _get_mobile_device(self):
        return MobileDevice(self.driver, self.driver.get_device_name())


class MobileDevice(object):
    __supported_devices = {
        "iPhone 6":
            {"ratio": 2,
             "width": 375,
             "height": 667,
             "fixed-border": {"top": 1, "bottom": 1},
             "crops":
                 {
                     "PORTRAIT": {"x": 0, "y": 70, "width": 375, "height": 623},
                     "LANDSCAPE": {"x": 0, "y": 70, "width": 667, "height": 264}
                 }
             },
        "iPhone 6 Plus":
            {"ratio": 3,
             "width": 414,
             "height": 736,
             "crops":
                 {
                     "PORTRAIT": {"x": 0, "y": 64, "width": 375, "height": 624},
                     "LANDSCAPE": {"x": 0, "y": 64, "width": 736, "height": 302}
                 }
             },
        "iPad (5th generation)":
            {"ratio": 2,
             "width": 768,
             "height": 1024,
             "fixed-border": {"top": 1, "bottom": 0},
             "crops":
                 {
                     "PORTRAIT": {"x": 0, "y": 70, "width": 768, "height": 1024},
                     "LANDSCAPE": {"x": 0, "y": 64, "width": 1024, "height": 768}
                 }
             }
    }

    __supported_platform = ["iOS"]

    def __init__(self, driver, device):
        self.driver = driver
        self.device = device

    def is_mobile(self):
        return self.device in self.__supported_devices

    def pixel_ratio(self):
        if self.device in self.__supported_devices:
            return self.__supported_devices[self.device]["ratio"]
        else:
            return 1

    def get_crops(self):
        if not self.is_mobile():
            return None
        else:
            return self.__supported_devices[self.device]["crops"]

    def get_fixed_border(self):
        if self.is_mobile() and "fixed-border" in self.__supported_devices[self.device]:
            return self.__supported_devices[self.device]["fixed-border"]
        else:
            return {"top": 0, "bottom": 0}


    @staticmethod
    def is_supported_device(device):
        return device in MobileDevice.__supported_devices

    @staticmethod
    def is_supported_platform(platformName):
        return platformName in MobileDevice.__supported_platform
