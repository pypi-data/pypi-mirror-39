import errno, os


class Root(object):

    def __init__(self, base_dir=None):
        if not base_dir:
            base_dir = os.getcwd()
        self.__root = base_dir
        self.__current_pwd = self.__root

    def root(self):
        return self.__root

    def mkdir(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise
