class EatsException(Exception):
    pass


class PageNotFoundError(EatsException):
    pass


class IAmNotOnPageError(EatsException):
    pass


class PageNameIsNoneError(EatsException):
    pass


class SearchByElementError(EatsException):
    pass


class ElementNotFoundError(EatsException):
    pass


class ElementClassError(EatsException):
    pass


class ElementRedefinedError(EatsException):
    pass


class WebElementNotFoundError(EatsException):
    pass


class MultipleWebElementsFoundError(EatsException):
    pass
