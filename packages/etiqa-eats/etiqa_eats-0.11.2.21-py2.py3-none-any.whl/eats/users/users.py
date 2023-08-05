from inspect import isclass

class Users(object):

    DEFAULT_USERNAME = 'default'

    def __init__(self, context):
        self._users = {}
        self._roles = {}
        #self._context = weakref.proxy(context) # avoid circular reference: see Users.setup(context)
        self._context = context
        self._current_user = None

    def __iter__(self):
        return iter(
            (name, user_obj) for name, user_obj in self._users.items()
        )

    def add(self, name, user_obj):
        if name == self.DEFAULT_USERNAME:
            user_obj._is_default = True
        user_obj._context = self._context
        self._users[name] = user_obj

    def get(self, name, set_current_user=True):
        user = self._users.get(name)
        if set_current_user:
            self._current_user = user
        return user

    @property
    def current_user(self):
        return self._current_user

    def add_role(self, name, cls):
        self._roles[name] = cls

    def get_role(self, name):
        return self._roles[name]

    @classmethod
    def setup(cls, context):
        context.users = cls(context)


class BaseUser(object):

    def __init__(self):
        self._is_default = False
        self._context = None
        self._applications = {}
        self._current_application = None

    @property
    def current_application(self):
        return self._current_application

    @current_application.setter
    def current_application(self, application):
        self._current_application = application
        if self._is_default:
            self._context.application = self.current_application

    def get_application(self, name):
        application = self._applications[name]
        if isclass(application):
            application = application.get_instance(self._context)
            self._applications[name] = application
        return application
