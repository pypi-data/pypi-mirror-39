from behave import *
from hamcrest import *
from eats.pyhamcrest import array_equal_to
from eats.utils.mapping import dict_reduce, table_mapping, dict_mapping


@then(u'{user_name:Username} should have "{name}" cookie set')
def step_impl(context, user_name, name):
    user = context.users.get(user_name)
    application = user.current_application
    cookie = application.driver.get_cookie(name)
    assert_that(cookie, not_none, "the cookie '{}' does not exists".format(name))


@then(u'{user_name:Username} should have "{name}" cookie with the following information')
def step_impl(context, user_name, name):
    user = context.users.get(user_name)
    application = user.current_application
    cookie = application.driver.get_cookie(name)
    assert_that(cookie, not_none, "the cookie '{}' does not exists".format(name))
    assert_that(len(context.table), equal_to(1), "table should contain only one row")
    keys = context.table.headings
    assert_that(dict_reduce(cookie, keys=keys), dict_mapping(context.table[0]))


@then(u'{user_name:Username} should have cookies with the following information')
def step_impl(context, user_name):
    user = context.users.get(user_name)
    application = user.current_application
    cookies = application.driver.get_cookies()
    assert_that(len(context.table), greater_than(0), "table should at least one row")
    keys = context.table.headings
    assert_that(table_mapping(cookies, keys=keys), array_equal_to(table_mapping(context.table)))