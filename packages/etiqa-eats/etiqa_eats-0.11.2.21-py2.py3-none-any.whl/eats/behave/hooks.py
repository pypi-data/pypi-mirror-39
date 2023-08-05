from eats.users.users import Users


def before_all(context):
    pass


def after_all(context):
    pass


def before_tag(context, tag):
    pass


def after_tag(context, tag):
    pass


def before_feature(context, feature):
    pass


def after_feature(context, feature):
    pass


def before_scenario(context, scenario):
    Users.setup(context)


def after_scenario(context, scenario):
    pass


def before_step(context, step):
    context.current_step = step


def after_step(context, step):
    pass