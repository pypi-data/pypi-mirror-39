import urllib
import copy


class RobotFileEats(object):

    def __init__(self, contents=None):
        self.__entries = []
        self.__contents = contents
        self.__parse(contents)

    def __parse(self, contents):
        """parse the input lines from a robots.txt file.
           We allow that a user-agent: line is not preceded by
           one or more blank lines."""
        lines = contents.split("\n")
        for line in lines:
            i = line.find('#')
            if i >= 0:
                line = line[:i]
            line = line.strip()
            if not line:
                continue
            line = line.split(':', 1)
            if len(line) == 2:
                line[1] = urllib.unquote(line[1].strip())
                if line[0] == "User-agent":
                        self._add_entry("User-agent", line[1])
                elif line[0] == "Disallow":
                    self._add_entry("Disallow", line[1])

                elif line[0] == "Allow":
                    self._add_entry("Allow", line[1])

                elif line[0] == "Sitemap":
                    self._add_entry("Sitemap", line[1])

    def _add_entry(self, entry, value):
        self.__entries.append({"entry": entry, "value": value})

    @property
    def entries(self):
        return copy.deepcopy(self.__entries)

    def __str__(self):
            return self.__contents

