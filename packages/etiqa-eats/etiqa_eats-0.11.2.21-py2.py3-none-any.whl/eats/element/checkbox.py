import six
from eats.utils import string_to_bool
from eats.element import Input


class Checkbox(Input):

    _element_type = "checkbox"

    def set_value(self, value):
        if self._bool(value) == (not self.is_checked()):
            self.click()

    def _bool(self, value):
        if type(value) is bool:
            return value
        else:
            value = six.text_type(value).lower()
            return string_to_bool(value)

    def get_value(self):
        return self.is_checked()

    def is_checked(self):
        return self.is_selected()

    def check(self):
        self.set_value(True)

    def uncheck(self):
        self.set_value(False)
