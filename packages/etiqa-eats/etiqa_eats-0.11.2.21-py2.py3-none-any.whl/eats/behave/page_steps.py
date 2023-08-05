from behave import *
from hamcrest import *
from eats.common.exceptions import IAmNotOnPageError
from ..users import Users


@given(u'I am on "{page}" page')
@given(u'{user_name:Username} is on "{page}" page')
def step_impl(context, page, user_name=Users.DEFAULT_USERNAME):
    user = context.users.get(user_name)
    application = user.current_application
    page = application.get_page(page)
    application.current_page = page
    page.goto()
    page_url = page.url
    current_url = application.current_url()
    assert_that(current_url, is_(equal_to(page_url)),
                u'The url is: "{}" instead of "{}"'.format(current_url, page_url))


@when(u'I go to "{page}" page')
@when(u'{user_name:Username} goes to "{page}" page')
def step_impl(context, page, user_name=Users.DEFAULT_USERNAME):
    user = context.users.get(user_name)
    application = user.current_application
    application.get_page(page).goto()


@then(u'{user_name:Username} should see "{title}" title on "{page}" page')
def step_impl(context, user_name, title, page):
    user = context.users.get(user_name)
    application = user.current_application
    page_title = application.get_page(page).get_title()
    assert_that(page_title, is_(equal_to(title)),
                u'The title is "{}" instead of "{}"'.format(page_title, title))


@then(u'{user_name:Username} should be on "{page}" page')
def step_impl(context, user_name, page):
    user = context.users.get(user_name)
    application = user.current_application
    page = application.get_page(page)
    im_on_page, message = page.i_am_on_page()
    assert_that(im_on_page, is_(True), message)
    application.current_page = page


@then(u'{user_name:Username} should not be on "{page}" page')
def step_impl(context, user_name, page):
    user = context.users.get(user_name)
    application = user.current_application
    page = application.get_page(page)
    im_on_page, message = page.i_am_on_page()
    assert_that(im_on_page, is_(False), message)


@then(u'{user_name:Username} should see "{value}" value on "{meta_name}" meta')
def step_impl(context, user_name, value, meta_name):
    user = context.users.get(user_name)
    application = user.current_application
    meta = application.current_page.get_meta_name_content(meta_name)
    assert_that(meta, is_(not_none()),
                u'The "{}" meta is not present on page'.format(meta_name))
    assert_that(meta, is_(equal_to(value)),
                u'Value of "{}" meta is "{}" value instead of "{}" value'.format(meta_name, meta, value))


@then(u'{user_name:Username} should see on "{meta_name}" meta the following value')
def step_impl(context, user_name, meta_name):
    user = context.users.get(user_name)
    application = user.current_application
    meta = application.current_page.get_meta_name_content(meta_name)
    assert_that(meta, is_(not_none()),
                u'The "{}" meta is not present on page'.format(meta_name))
    assert_that(meta, is_(equal_to(context.text)),
                u'Value of "{}" meta is "{}" value instead of "{}" value'.format(meta_name, meta, context.text))


@then(u'{user_name:Username} should not see "{meta_name}" meta')
def step_impl(context, user_name, meta_name):
    user = context.users.get(user_name)
    application = user.current_application
    meta = application.current_page.get_meta_name_content(meta_name)
    assert_that(meta, is_(none()),
                u'The "{}" meta is present on page'.format(meta_name))
