from eats.utils.root import Root
import os


class WorkSpace(Root):

    def __init__(self, base_dir=None):
        super(WorkSpace, self).__init__(base_dir)
        self.__root = super(WorkSpace, self).root() + "/workspace"
        self.__current_pwd = self.__root
        if not os.path.exists(self.__current_pwd):
            self.mkdir(self.__current_pwd)

    def root(self):
        return self.__root

    def parent_root(self):
        return super(WorkSpace, self).root()

    def change_cwd(self, relative_path):
        self.__current_pwd = self.root() + relative_path
        self.mkdir(self.__current_pwd)

    def cwd(self):
        return self.__current_pwd

