import time
import math
from eats.page.page import Page


class ReactPage(Page):

    def __init__(self, driver, url, timeout_millisec=0):
        super(ReactPage, self).__init__(driver, url)
        self.timeout_millisec = timeout_millisec

    def i_am_on_page(self):
        POLL_PERIOD_MILLISEC = 100.0
        wait_iterations = math.floor(self.timeout_millisec / POLL_PERIOD_MILLISEC)
        current = self.current_url()
        while current != self.url and (wait_iterations > 0):
            wait_iterations -= 1
            time.sleep(POLL_PERIOD_MILLISEC / 1000.0)
            current = self.current_url()
        if current != self.url:
            return False, 'The url is: "%s" instead of "%s"' % (current, self._url)
        return True, 'I am on page %s' % self.name
