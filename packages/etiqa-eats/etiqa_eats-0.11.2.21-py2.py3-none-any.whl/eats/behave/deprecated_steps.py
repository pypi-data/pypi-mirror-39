import urllib
from behave import *
from hamcrest import *
from eats.pyhamcrest import array_equal_to_by_key, array_equal_to
from eats.utils.sitemap import sitemap_parser, replace_env_url_to_prod, SiteMapGen, url_encode
from eats.utils.robots import RobotFileEats
from eats.utils.google_site_verification import GoogleSiteVerification
from eats.utils.bing import bing_parser
from eats.utils.mapping import table_mapping


@then(u'{user_name:Username} should have the following google tracking keys information')
def step_impl(context, user_name):
    user = context.users.get(user_name)
    application = user.current_application
    keys = context.table.headings
    ga = application.driver.get_google_tracking_keys()
    assert_that(table_mapping(ga, keys=keys), array_equal_to(table_mapping(context.table)))


@then(u'{user_name:Username} should have the following information on sitemap.xml')
def step_impl(context, user_name):
    user = context.users.get(user_name)
    application = user.current_application
    application.go_to_url('/sitemap.xml')
    contents = application.get_page_source()
    sitemap = sitemap_parser(contents)
    prod_netloc = context.application.prod_netloc
    keys = ["loc", "lastmod", "priority", "changefreq"]
    trans = lambda page: url_encode(replace_env_url_to_prod(application.get_page(page).url_without_fragment, prod_netloc))
    expected = table_mapping(context.table, maps={"page": "loc"}, keys=keys, transform={"page": trans})
    gen_sitemap = SiteMapGen(expected)
    gen_sitemap.write_xml(context.workspace.cwd() + "/sitemap.xml")
    print(expected)
    assert_that(sitemap, array_equal_to_by_key(expected, "loc"))


@then(u'{user_name:Username} should have the following information on BingSiteAuth.xml')
def step_impl(context, user_name):
    user = context.users.get(user_name)
    application = user.current_application
    application.go_to_url('/BingSiteAuth.xml')
    contents = application.get_page_source()
    bing = bing_parser(contents)
    assert_that(bing, array_equal_to_by_key(table_mapping(context.table), "user"))


@then(u'{user_name:Username} should have the following information on robots.txt')
def step_impl(context, user_name):
    user = context.users.get(user_name)
    application = user.current_application
    application.go_to_url('/robots.txt')
    f = urllib.urlopen(application.current_url())
    contents = f.read()
    robots = RobotFileEats(contents)
    expected = [{"entry": x["ENTRY"], "value": x["VALUE"]} for x in context.table]
    assert_that(robots.entries, array_equal_to(expected))


@then(u'{user_name:Username} should have the following information on "{relative_path}" google site verification')
def step_impl(context, user_name, relative_path):
    user = context.users.get(user_name)
    application = user.current_application
    application.go_to_url(relative_path)
    f = urllib.urlopen(application.current_url())
    contents = f.read()
    gsv = GoogleSiteVerification(contents)
    expected = [{"entry": x["ENTRY"], "value": x["VALUE"]} for x in context.table]
    assert_that(gsv.entries, array_equal_to(expected))
