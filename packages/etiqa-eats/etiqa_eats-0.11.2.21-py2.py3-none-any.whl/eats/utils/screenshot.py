import base64
import os
import time
from eats.utils.cropper import Cropper


class Screenshot(object):

    def __init__(self, window, strategy=None):
        self.driver = window.driver
        self.window = window
        if strategy:
            self.strategy = strategy
        else:
            self.strategy = ScreenshotBaseStrategy(window)

    def get_page_screenshot(self, file_name):
        self.strategy.screenshots(file_name)
        self.__json_meta_data(file_name)

    def get_screenshot(self, file_name):
        base64_encoded_data = self.driver.get_screenshot_as_base64()
        binary_data = base64.b64decode(base64_encoded_data)
        with open(file_name, "wb") as fh:
            fh.write(binary_data)
        self.clean_screenshot(file_name)
        self.__json_meta_data(file_name)

    def clean_screenshot(self, image_path):
        image = Cropper.image(image_path)
        crops = self.window.get_crops()
        image = Cropper.crop(image, crops["x"], crops["y"],  crops["width"], crops["height"])
        Cropper.save(image, image_path)

    def __json_meta_data(self, file_name):
        root, ext = os.path.splitext(file_name)
        file_json = root + ".json"
        image = os.path.basename(file_name)
        width = self.window.get_width()
        height = self.window.get_height()
        data = {
            'meta': {},
            'properties': {
                    'resolution': "{}x{}".format(width, height),
                    'browser': self.driver.get_browser_name(),
                    'platform name': self.driver.get_platform_name(),
                    'device name': self.driver.get_device_name()
                },
            'screenshotName': image,
            'filename': image,
            'file': image
            }
        import json
        with open(file_json, 'w') as outfile:
            json.dump(data, outfile)


class ScreenshotBaseStrategy(object):

    def __init__(self, window):
        self.driver = window.driver
        self.window = window

    def screenshots(self, file_name):
        self.window.scroll_to_top()
        if self.get_total_height_to_scroll() != 0:
            frames = 0
            files = []
            scroll = 0
            offset = 0
            attempts = 0
            file_name_tupla = file_name.split(".")
            while not self.window.is_bottom_page():
                self.window.scroll_by((0, scroll))
                while self.window.offset_position() < offset:
                    time.sleep(0.1)
                    attempts += 1
                    if attempts == 5:
                        raise Exception('The page is not scrolling')
                height = self.window.page_height()
                file_screenshot = file_name_tupla[0] + "_" + str(frames) + "_." + file_name_tupla[1]
                self.get_screenshot(file_screenshot)
                self.cut_strategy(scroll, height, file_screenshot)
                files.append(file_screenshot)
                scroll = self.calculate_scroll()
                offset += scroll
                frames += 1
            Cropper.merge_images(file_name, files)
            self._remove_files(files)
        else:
            self.get_screenshot(file_name)

    def cut_strategy(self, scroll, height, file_screenshot):
        if not self.window.is_bottom_page():
            self.cut_bottom(file_screenshot)
        if self.window.is_bottom_page():
            self.cut_last_frame(file_screenshot, scroll)
        elif not self.window.is_top_page():
            self.cut_top(file_screenshot)

    def calculate_scroll(self):
        borders = self.window.get_fixed_border()
        total_borders = borders["top"] + borders["bottom"]
        scroll = self.window.page_height() - total_borders
        scroll_left = self.get_total_height_to_scroll()
        if scroll < scroll_left:
            return scroll
        else:
            return scroll_left

    def get_total_height_to_scroll(self):
        return self.window.page_max_height() - self.window.get_total_scroll()

    def get_screenshot(self, file_path):
        base64_encoded_data = self.driver.get_screenshot_as_base64()
        binary_data = base64.b64decode(base64_encoded_data)
        with open(file_path, "wb") as fh:
            fh.write(binary_data)
        self.clean_screenshot(file_path)

    def clean_screenshot(self, image_path):
        image = Cropper.image(image_path)
        crops = self.window.get_crops()
        image = Cropper.crop(image, crops["x"], crops["y"],  crops["width"], crops["height"])
        Cropper.save(image, image_path)

    def cut_last_frame(self, file_name, scroll):
        borders = self.window.get_fixed_border()
        pixels = borders["top"]
        not_fixed = self.window.page_height() - (borders["top"] + borders["bottom"])
        img = Cropper.image(file_name)
        cuts = pixels + (not_fixed - scroll)
        img2 = Cropper.crop_top(img, self.convert_size_ratio(cuts))
        img2.save(file_name)

    def cut_top(self, file_name):
        borders = self.window.get_fixed_border()
        pixels = borders["top"]
        img = Cropper.image(file_name)
        img2 = Cropper.crop_top(img, self.convert_size_ratio(pixels))
        img2.save(file_name)

    def cut_bottom(self, file_name):
        borders = self.window.get_fixed_border()
        pixels = borders["bottom"]
        img = Cropper.image(file_name)
        img2 = Cropper.crop_bottom(img, self.convert_size_ratio(pixels))
        img2.save(file_name)

    def _remove_files(self, files):
        for image in files:
            os.remove(image)

    def convert_size_ratio(self, size):
        pixel_ratio = self.window.pixel_ratio()
        return size * pixel_ratio

    def convert_sizes_ratio(self, sizes):
        pixel_ratio = self.window.pixel_ratio()
        return sizes[0] * pixel_ratio, sizes[1] * pixel_ratio


class ScreenshotFixedPositionStrategy(ScreenshotBaseStrategy):

    def screenshots(self, file_name):
        self.window.scroll_to_top()
        if self.get_total_height_to_scroll() != 0:
            frames = 0
            files = []
            scroll = 0
            offset = 0
            attempts = 0
            file_name_tupla = file_name.split(".")
            while not self.window.is_bottom_page():
                self.window.scroll_by((0, scroll))
                while self.window.offset_position() < offset:
                    time.sleep(0.1)
                    attempts += 1
                    if attempts == 5:
                        raise Exception('The page is not scrolling')
                height = self.window.page_height()
                file_screenshot = file_name_tupla[0] + "_" + str(frames) + "_." + file_name_tupla[1]
                self.get_screenshot(file_screenshot)
                self.cut_strategy(scroll, height, file_screenshot)
                files.append(file_screenshot)
                scroll = self.calculate_scroll()
                offset += scroll
                frames += 1
            Cropper.merge_images(file_name, files)
            self._remove_files(files)
        else:
            self.get_screenshot(file_name)

    def cut_strategy(self, scroll, height, file_screenshot):
        if not self.window.is_bottom_page():
            self.cut_bottom(file_screenshot)
        if self.window.is_bottom_page():
            self.cut_last_frame(file_screenshot, scroll)
        elif not self.window.is_top_page():
            self.cut_top(file_screenshot)

    def calculate_scroll(self):
        scroll = self.window.page_height() - self.__get_fixed_position_elements_height()
        scroll_left = self.__total_height_to_scroll()
        if scroll < scroll_left:
            return scroll
        else:
            return scroll_left

    def __get_fixed_position_elements_height(self):
        elements = self.driver.find_elements_with_fixed_position()
        total = 0
        position_y = 0
        for element in elements:
            coords = self.driver.get_element_coordinate(element)
            if coords['x'] + coords['width'] > 0 and coords['y'] + coords['height'] > 0:
                shadow = self.driver.get_element_shadow(element)
                if position_y >= coords["y"] and coords["height"] != 0:
                    height = coords["height"] - (position_y - coords["y"]) + shadow.get("height", 0)
                    position_y = coords["y"] + coords["height"]
                elif coords["height"] != 0:
                    height = coords["height"] + shadow.get("height", 0)
                    position_y = coords["y"] + coords["height"]
                else:
                    height = 0
                total += height
        borders = self.window.get_fixed_border()
        total = total + borders["top"] + borders["bottom"]
        return total

    def __total_height_to_scroll(self):
        return self.window.page_scroll_height() - self.window.get_total_scroll()

    def __calculate_not_fixed_area(self):
        return self.window.page_height() - self.__get_fixed_position_elements_height()

    def __calculate_fixed_top(self):
        elements = self.driver.find_elements_with_fixed_position()
        position_y = 0
        height = 0
        for element in elements:
            coords = self.driver.get_element_coordinate(element)
            if coords['x'] + coords['width'] > 0 and coords['y'] + coords['height'] > 0:
                shadow = self.driver.get_element_shadow(element)
                if position_y >= coords["y"] and coords["height"] != 0:
                    position_y = coords["y"] + coords["height"]
                height = position_y + shadow.get("height", 0)

        borders = self.window.get_fixed_border()
        height = height + borders["top"]
        return height

    def __calculate_fixed_bottom(self):
        height = 0
        elements = self.driver.find_elements_with_fixed_position()
        for element in elements:
            coords = self.driver.get_element_coordinate(element)
            if coords["y"] + coords["height"] == self.window.page_height():
                shadow = self.driver.get_element_shadow(element)
                height = coords["height"] + shadow.get("height", 0)
        borders = self.window.get_fixed_border()
        height = height + borders["bottom"]
        return height

    def cut_last_frame(self, file_name, scroll):
        pixels = self.__calculate_fixed_top()
        not_fixed = self.__calculate_not_fixed_area()
        img = Cropper.image(file_name)
        cuts = pixels + (not_fixed - scroll)
        img2 = Cropper.crop_top(img, self.convert_size_ratio(cuts))
        img2.save(file_name)

    def cut_top(self, file_name):
        pixels = self.__calculate_fixed_top()
        img = Cropper.image(file_name)
        img2 = Cropper.crop_top(img, self.convert_size_ratio(pixels))
        img2.save(file_name)

    def cut_bottom(self, file_name):
        pixels = self.__calculate_fixed_bottom()
        img = Cropper.image(file_name)
        img2 = Cropper.crop_bottom(img, self.convert_size_ratio(pixels))
        img2.save(file_name)
