import os
from six.moves import configparser


class Configurator(object):

    def __init__(self):
        root = os.getcwd() + "/eats.ini"
        self.config = configparser.ConfigParser()
        self.config.read(root)

    @classmethod
    def setup(cls, context):
        context.eats = cls()
