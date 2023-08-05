import behave
from behave import *
from ..common.utils import parse_word
from ..users import Users

behave.register_type(a_=parse_word(r'a|an'))

@given(u'I am {:a_} "{role}"')
@given(u'{user_name:Username} is {:a_} "{role}"')
def step_impl(context, a_, role, user_name=Users.DEFAULT_USERNAME):
    users = context.users
    role = users.get_role(role)
    user = role()
    users.add(user_name, user)

@given(u'I am on "{application}" website')
@given(u'{user_name:Username} is on "{application}" website')
def step_impl(context, application, user_name=Users.DEFAULT_USERNAME):
    users = context.users
    user = users.get(user_name)
    application = user.get_application(application)
    user.current_application = application