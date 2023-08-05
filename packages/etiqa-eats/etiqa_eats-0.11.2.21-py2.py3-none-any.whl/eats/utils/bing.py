from bs4 import BeautifulSoup as Soup


def bing_parser(contents):
    soup = Soup(contents, "lxml")

    # find all the <url> tags in the document
    users = soup.findAll('user')

    # no urls? bail
    if not users:
        return False

    # storage for later...
    out = []

    for user in users:
        u = user.string
        out.append({"user": u})
    return out


class BingSiteAuth(object):
    def __init__(self, users):
        self._users = users

    def write_xml(self, path):
        of = open(path, 'w')
        of.write('<?xml version="1.0" "?>\n')
        of.write('<users>\n')
        user_str = '<user>{}</user>\n'
        for exp in self.users:
            of.write(user_str.format(exp))
        of.write('</users>')
        of.close()
