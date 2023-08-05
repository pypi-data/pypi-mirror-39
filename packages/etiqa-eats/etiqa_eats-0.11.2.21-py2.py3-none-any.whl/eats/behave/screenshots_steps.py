from behave import *
import os.path
from eats.utils.naming import Naming
from eats.users import Users


@given(u'{user_name:Username} has the browser "{resolution}" resolution')
@given(u'I have the browser "{resolution}" resolution')
def step_impl(context, resolution, user_name=Users.DEFAULT_USERNAME):
    user = context.users.get(user_name)
    application = user.current_application
    window = application.driver.window
    if not window.is_mobile():
        window.set_default(resolution.split("x"))
        window.resize_default()


@when(u'{user_name:Username} takes "{page}" page screenshot')
@when(u'I take "{page}" page screenshot')
def step_impl(context, page, user_name=Users.DEFAULT_USERNAME):
    if user_name == 'default':
        context.execute_steps(u"""
            When I take "{page}" page screenshot with "{prefix}" prefix
        """.format(page=page, prefix="page"))
    else:
        context.execute_steps(u"""
                    When {user_name} takes "{page}" page screenshot with "{prefix}" prefix
                """.format(page=page, prefix="page", user_name="{" + user_name + "}"))


@when(u'{user_name:Username} takes "{page}" page screenshot with "{prefix}" prefix')
@when(u'I take "{page}" page screenshot with "{prefix}" prefix')
def step_impl(context, page, prefix, user_name=Users.DEFAULT_USERNAME):
    if not hasattr(context, "workspace"):
        assert False, "Workspace is not defined in context"
    user = context.users.get(user_name)
    application = user.current_application
    window = application.driver.window
    dvr = application.driver
    browser_info = dvr.get_platform_name() + "-" + dvr.get_device_name() + "-" + dvr.get_browser_name() + "-" + str(
        window.get_width()) + "px"
    page_obj = application.get_page(page)
    file_name = browser_info + "-" + page_obj.name + "-" + prefix
    file_name = Naming.clean_filename(file_name.lower())
    if not os.path.exists(context.workspace.cwd() + "/actual/"):
        os.makedirs(context.workspace.cwd() + "/actual")
    page_obj.get_full_screenshot(context.workspace.cwd() + "/actual/" + file_name + ".png")
