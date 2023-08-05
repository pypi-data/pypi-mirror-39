from eats.element import Element


class Input(Element):
    
    _element_type = "input_type"

    def __init__(self, *args, **kwargs):
        super(Input, self).__init__(*args, **kwargs)
        self._set_validation_error_element()

    def __eq__(self, other_input_text):
        return self.get_value() == other_input_text.get_value()

    def get_value(self):
        return self.get_attribute('value')

    def set_value(self, value):
        self.clear()
        self.send_keys(value)

    def get_placeholder(self):
        return self.get_attribute('placeholder')

    @property
    def error(self):
        return self._error
    
    def _set_validation_error_element(self):
        element = self._validation_error_element()
        if element is not None and not isinstance(element, ValidationError):
            raise TypeError("error element should be a %s but is a %s" % (ValidationError, type(element)))
        self._error = element

    def _validation_error_element(self):
        return None


class ValidationError(Element):

    _element_type = "validation_error"

    @property
    def message(self):
        #return self.get_attribute("innerHTML")
        return self.text
