from hamcrest.core.base_matcher import BaseMatcher


class ArrayIsEqualByKey(BaseMatcher):

    def __init__(self, equals, key):
        self.object = equals
        self.key = key
        self._pass = True
        self._error = u""

    def status(self):
        return self._pass

    def matches(self, item, mismatch_description=None):
        self._pass = True
        for element in self.object:
            search_in = [x for x in item if x[self.key] == element[self.key]]
            if len(search_in) == 1:
                evaluate = u""
                for key in element:
                    actual = search_in[0][key]
                    if actual != element[key]:
                        evaluate += u"key '{}' should be '{}' but was '{}' ".format(key, element[key], actual)
                if evaluate != u"":
                    self.error(u"item '{}': ".format(element[self.key]) + evaluate)
            elif len(search_in) > 1:
                self.error(u"item '{}' should have only '1' entry instead of '{}'".format(element[self.key], len(search_in)))
            else:
                self.error(u"item '{}' should be present".format(element[self.key]))
        for x in item:
            if len([y for y in self.object if y[self.key] == x[self.key]]) == 0:
                self.error(u"item key value '{}' should not be present".format(x[self.key]))

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


def array_equal_to_by_key(obj, key):
    """Matches if array array dict is equal to a given object.

    :param obj: The object to compare against as the expected value.

    This matcher compares the evaluated object to ``obj`` for equality."""
    return ArrayIsEqualByKey(obj, key)


