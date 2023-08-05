import six
if six.PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin
from behave import *
from hamcrest import *
from eats.common.utils import is_absolute_url
from ..users import Users


@when(u'I go to "{url}" url')
@when(u'{user_name:Username} goes to "{url}" url')
def step_impl(context, url, user_name=Users.DEFAULT_USERNAME):
    user = context.users.get(user_name)
    application = user.current_application
    application.go_to_url(url)


@then(u'{user_name:Username} should be on "{url}" url')
def step_impl(context, user_name, url):
    user = context.users.get(user_name)
    application = user.current_application
    if not is_absolute_url(url):
        url = _make_absolute(url, application.base_url)
    assert_that(application.current_url(), is_(equal_to(url)),
                'I am on "{}" url instead of "{}" url'.format(application.current_url(), url))


def _make_absolute(url, base_url):
    return urljoin(base_url, url)
