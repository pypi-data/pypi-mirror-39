from hamcrest.core.base_matcher import BaseMatcher


class ArrayIsEqual(BaseMatcher):

    def __init__(self, equals):
        self.object = equals
        self._pass = True
        self._error = u""

    def status(self):
        return self._pass

    def matches(self, item, mismatch_description=None):
        self._pass = True
        for element in self.object:
            search_in = [x for x in item if x == element]
            if len(search_in) == 0:
                self.error(u"item {} should be present".format(element))
            elif len(search_in) > 1:
                self.error(u"item {} should have entries instead of {}".format(element, len(search_in)))
        for x in item:
            if len([y for y in self.object if y == x]) == 0:
                self.error(u"item key value {} should not be present".format(x))

        match_result = self.status()
        if not match_result and mismatch_description:
            self.error(item, mismatch_description)
        return match_result

        return not self._failed

    def error(self, message):
        self._pass = False
        self._error += message + u"\n"

    def describe_to(self, description):
        description.append_text(self._error)


def array_equal_to(obj):
    """Matches if array array dict is equal to a given object.

    :param obj: The object to compare against as the expected value.

    This matcher compares the evaluated object to ``obj`` for equality."""
    return ArrayIsEqual(obj)


