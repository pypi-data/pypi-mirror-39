from behave import *
from hamcrest import *
from selenium.common.exceptions import RemoteDriverServerException
from eats.pyhamcrest import array_equal_to_by_key
from eats.utils.mapping import table_mapping
from ..users import Users


@when(u'I press "{key}" key')
@when(u'{user_name:Username} presses "{key}" key')
def step_impl(context, key, user_name=Users.DEFAULT_USERNAME):
    user = context.users.get(user_name)
    application = user.current_application
    assert_that(
        calling(application.driver.send_special_key).with_args(key),
        not(raises(RemoteDriverServerException)),
        "{unsupported} key is not supported".format(unsupported=key)
    )


@then(u'{user_name:Username} should have "{name}" meta contents element')
def step_impl(context, user_name, name):
    user = context.users.get(user_name)
    application = user.current_application
    contents = application.driver.get_metadata_elements_content_by_name(name)
    keys = context.table.headings
    assert_that(table_mapping(contents, keys=keys), array_equal_to_by_key(table_mapping(context.table), "content"))