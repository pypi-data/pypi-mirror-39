import six
if six.PY2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse
import parse


def get_root_url(url):
    url_obj = urlparse(url)
    final_res = url_obj.scheme + "://" + url_obj.netloc + "/"
    return final_res

def is_absolute_url(url):
    return bool(urlparse(url).netloc)

def parse_word(word):
    @parse.with_pattern(word)
    def _parse_word(text):
        return text.strip()

    return _parse_word
