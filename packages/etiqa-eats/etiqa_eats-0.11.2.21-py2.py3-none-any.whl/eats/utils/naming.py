import os
import unicodedata
import string


class Naming(object):

    @staticmethod
    def covert_url_to_name(url):
        if url == "/":
            return "homepage"
        else:
            url, file_extension = os.path.splitext(url)
            if file_extension:
                file_extension = file_extension.replace(".", "_")
            url = url.replace("/", "_")
            if url.startswith(""):
                url = url[1:]
            if url.endswith("_"):
                url = url[:-1]
        return url + file_extension

    @staticmethod
    def covert_path_to_name(path):
        return path.replace("/", "_").replace(".", "_")

    @staticmethod
    def clean_filename(filename, replace=' '):
        whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)
        # replace spaces
        for r in replace:
            filename = filename.replace(r, '_')

        # keep only valid ascii chars
        cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

        # keep only whitelisted chars

        return ''.join(c for c in cleaned_filename if c in whitelist)
