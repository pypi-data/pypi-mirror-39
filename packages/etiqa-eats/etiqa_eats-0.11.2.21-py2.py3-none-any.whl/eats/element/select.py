from eats.element import Input


class Select(Input):
    """Select Field Element"""
    _element_type = "select_type"

    def __get_options(self):
        return self.find_elements_by_xpath("//option")

    """Set the value"""
    def set_value(self, value):
        self._set_value_by_condition(lambda option: option.get_attribute('value') == value)

    """Set value by label"""
    def set_value_by_label(self, label):
        self._set_value_by_condition(lambda option: option.text == label)

    def _set_value_by_condition(self, condition):
        for option in self.__get_options():
            if condition(option):
                option.click()

    """Gets the value"""
    def get_value(self):
        return self.get_attribute('value')

    """Gets the selected value label"""
    def get_selected_option_label(self):
        value = self.get_value()
        options = self.__get_options()
        for option in options:
            if option.get_attribute('value') == value:
                return option.text

    def get_options_values(self):
        return [option.get_attribute('value') for option in self.__get_options()]

    def get_options_labels(self):
        return [option.text for option in self.__get_options()]
