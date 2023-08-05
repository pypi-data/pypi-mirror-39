import urllib
import copy


class GoogleSiteVerification(object):

    def __init__(self, contents=None):
        self.__entries = []
        self.__contents = contents
        self.__parse(contents)

    def __parse(self, contents):
        lines = contents.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line.split(':', 1)
            if len(line) == 2:
                line[1] = urllib.unquote(line[1].strip())
                if line[0] == "google-site-verification":
                        self._add_entry("google-site-verification", line[1])

    def _add_entry(self, entry, value):
        self.__entries.append({"entry": entry, "value": value})

    @property
    def entries(self):
        return copy.deepcopy(self.__entries)

    def __str__(self):
            return self.__contents

