import six
from eats.utils import string_to_bool
from eats.element import Input


class Radio(Input):

    _element_type = "radio"

    def set_value(self, value):
        if self._bool(value) == (not self.is_selected()):
            self.click()

    def _bool(self, value):
        if type(value) is bool:
            return value
        else:
            value = six.text_type(value).lower()
            return string_to_bool(value)

    def get_value(self):
        return self.is_selected()

    def select(self):
        self.set_value(True)
