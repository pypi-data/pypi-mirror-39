__author__ = 'pulphix'

from .custom_types import register_custom_types
register_custom_types()
del register_custom_types

from . import page_steps
from . import application_steps
from . import cookies_steps
from . import element_steps
from . import driver_steps

from . import screenshots_steps
from . import user_steps

from . import deprecated_steps
