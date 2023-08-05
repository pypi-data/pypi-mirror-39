from eats.common.exceptions import ElementNotFoundError, ElementRedefinedError

class CompositeElement(object):

    def __init__(self):
        self._elements = {}
        self._load_elements()

    def _load_elements(self):
        pass

    def get_element(self, name):
        try:
            return self._elements[name]
        except KeyError as e:
            raise ElementNotFoundError(e)

    def add_element(self, name, element, add_sub_elements=True):
        if name in self._elements:
            raise ElementRedefinedError(name)
        el = self._instantiate_element(element)
        self._elements[name] = el
        if add_sub_elements:
            self._add_sub_elements(el)

    def _instantiate_element(self, element):
        if isinstance(element, (tuple, list)):
            element_obj = self._instantiate_element_from_list(list(element))
        else:
            element_obj = element
        return element_obj

    def _instantiate_element_from_list(self, *args):
        raise NotImplementedError

    def _add_sub_elements(self, element):
        for (name, sub_element) in element.get_elements():
            # BUGFIX: avoid recursive calls to _add_sub_elements
            self.add_element(name, sub_element, False)

    def get_elements(self):
        return ((name, self.get_element(name)) for name in self._elements)