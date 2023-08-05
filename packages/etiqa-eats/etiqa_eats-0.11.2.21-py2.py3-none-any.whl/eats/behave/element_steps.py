from behave import *
from hamcrest import *
from selenium.common.exceptions import NoSuchElementException
from eats.common.exceptions import SearchByElementError, ElementNotFoundError
from eats.element import Input
from ..users import Users


# TODO: see https://github.com/behave/behave.example/blob/master/step_matcher.features/steps/step_optional_part.py
@when(u'I click "{element}" element')
@when(u'{user_name:Username} clicks "{element}" element')
def step_impl(context, element, user_name=Users.DEFAULT_USERNAME):
    user = context.users.get(user_name)
    application = user.current_application
    try:
        application.current_page.get_element(element).click()
    except ElementNotFoundError:
        raise AssertionError("Element not present on Page Object")
    except SearchByElementError:
        raise AssertionError("Element search by method not supported")


@when(u'I set the value "{value:PossiblyEmpty}" on "{input_element}" element')
@when(u'{user_name:Username} sets the value "{value:PossiblyEmpty}" on "{input_element}" element')
def step_impl(context, value, input_element, user_name=Users.DEFAULT_USERNAME):
    user = context.users.get(user_name)
    application = user.current_application
    current_page = application.current_page
    input_element = current_page.get_element(input_element)
    input_element.set_value(value)


@then(u'{user_name:Username} should see "{value:PossiblyEmpty}" value in "{element}" element')
def step_impl(context, user_name, value, element):
    user = context.users.get(user_name)
    application = user.current_application
    current_page = application.current_page
    element = current_page.get_element(element)
    assert element.is_displayed(), "Element is not present in {}".format(current_page.name)
    assert element.get_value() == value, "Element value should be '{}', but is '{}'".format(value, element.get_value())


@then(u'{user_name:Username} should see "{element}" element')
def step_impl(context, user_name, element):
    user = context.users.get(user_name)
    application = user.current_application
    try:
        current_page = application.current_page
        assert_that(current_page, is_(not_none()), "Current page has not been set")
        element = current_page.get_element(element)
        assert element.is_displayed(), "Element is not {} in {}".format(
            "visible" if element.is_present() else "present", current_page.name)
    except ElementNotFoundError:
        raise AssertionError("Element not present on Page Object")
    except NoSuchElementException:
        raise AssertionError("Element not present on Page")
    except SearchByElementError:
        raise AssertionError("Element search by method not supported")


@then(u'{user_name:Username} should not see "{element}" element')
def step_impl(context, user_name, element):
    user = context.users.get(user_name)
    application = user.current_application
    try:
        current_page = application.current_page
        assert_that(current_page, is_(not_none()), "Current page has not been set")
        element = current_page.get_element(element)
        assert not element.is_displayed(), "Element is displayed in {}".format(current_page.name)
    except NoSuchElementException:
        pass #Element not present on Page
    except ElementNotFoundError:
        raise AssertionError("Element not present on Page Object")
    except SearchByElementError:
        raise AssertionError("Element search by method not supported")


@then(u'"{element}" element should contain "{sub_element}" sub element')
def step_impl(context, element, sub_element):
    try:
        current_page = context.application.current_page
        assert_that(current_page, is_(not_none()), "Current page has not been set")
        element = current_page.get_element(element)
        sub_element = element.get_element(sub_element)
        assert sub_element.is_displayed(), "Element is not {} within {}".format(
            "visible" if sub_element.is_present() else "present", element)
    except ElementNotFoundError:
        raise AssertionError("Element not present on {} Object".format(element))
    except NoSuchElementException:
        raise AssertionError("Element not present on {}".format(element))
    except SearchByElementError:
        raise AssertionError("Element search by method not supported")

@then(u'"{element}" element should not contain "{sub_element}" sub element')
def step_impl(context, element, sub_element):
    try:
        current_page = context.application.current_page
        assert_that(current_page, is_(not_none()), "Current page has not been set")
        element = current_page.get_element(element)
        sub_element = element.get_element(sub_element)
        assert not sub_element.is_displayed(), "Element is displayed within {}".format(element)
    except NoSuchElementException:
        pass #Element not present on Page
    except ElementNotFoundError:
        raise AssertionError("Element not present on Page Object")
    except SearchByElementError:
        raise AssertionError("Element search by method not supported")


@then(u'"{input_element}" element should display error message "{error_message}"')
def step_impl(context, input_element, error_message):
    current_page = context.application.current_page
    input_element = current_page.get_element(input_element)
    assert_that(input_element, is_(instance_of(Input)),
        "input_element must be an instance of {}".format(Input))
    assert_that(input_element.error.is_displayed(), is_(True))
    assert_that(input_element.error.message, is_(equal_to(error_message)))


@then(u'"{input_element}" element should not display any error messages')
def step_impl(context, input_element):
    current_page = context.application.current_page
    input_element = current_page.get_element(input_element)
    assert_that(input_element, is_(instance_of(Input)),
        "input_element must be an instance of {}".format(Input))
    assert_that(input_element.error.is_displayed(), is_(False))
