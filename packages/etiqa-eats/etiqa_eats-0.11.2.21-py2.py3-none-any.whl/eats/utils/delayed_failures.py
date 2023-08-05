"""
Setup delayed failures:

call this module's before_all, before_scenario and before_step functions
from behave's environment.py module

Usage:

inside a step definition, you'll be writing something like:

    ...
    context.delayed_assert_that(
        hamcrest_arg1,
        hamcrest_arg2,
        hamcrest_arg3
    )

"""


import json
import os
from decimal import Decimal
from functools import partial
from textwrap import dedent

import behave.step_registry
import behave.model
import hamcrest
from hamcrest import is_
import six


def assert_that(arg1, arg2=None, arg3='', handler=None):
    try:
        hamcrest.assert_that(arg1, arg2, arg3)
    except AssertionError as e:
        if not handler:
            raise
        else:
            message = e.args[0]
            handler(message)


def _check_delayed_failures_step_impl(context):
    delayed_failures = context._delayed_failures
    delayed_failures_found = delayed_failures.delayed_failures_exist()
    assert not delayed_failures_found, (
        'Delayed failures found.\n\n' + delayed_failures.pretty_print())


def before_all(context):
    step = behave.model.Step(
        '',
        0,
        u'Then',
        u'then',
        u'the test will check no delayed failures exist'
    )
    registry = getattr(context._runner, 'step_registry', behave.step_registry.registry)
    registry.add_step_definition(
        step.step_type,
        step.name,
        _check_delayed_failures_step_impl
    )
    context._check_delayed_failures_step = step


def before_scenario(context, scenario, delayed_failures_instance):
    userdata_option = context.config.userdata.get('delay_failures', 'false').lower()
    globally_enabled = userdata_option in ('true', 'yes', 'y')
    enabled_for_this_scenario = ('delay_failures' in scenario.effective_tags)
    enabled = globally_enabled or enabled_for_this_scenario
    assertion_error_handler = None
    if enabled:
        assertion_error_handler = delayed_failures_instance.add_delayed_failure
        scenario.steps.append(context._check_delayed_failures_step)
        context._delayed_failures = delayed_failures_instance
    context.delayed_assert_that = partial(assert_that, handler=assertion_error_handler)


def before_step(context, step):
    context.current_step = step


class DelayedFailures(object):

    def get_delayed_failures(self):
        raise NotImplementedError

    def save_delayed_failure(self, failure):
        raise NotImplementedError

    def delayed_failures_exist(self):
        raise NotImplementedError

    def __init__(self, context):
        self._context = context

    def add_delayed_failure(self, message):
        if not isinstance(message, (str, six.text_type)):
            message = six.text_type(message)
        failure = {
            'step': self._context.current_step.name,
            'location': str(self._context.current_step.location),
            'message': message
        }
        self.save_delayed_failure(failure)

    def pretty_print(self):
        result = []
        for index, failure in enumerate(self.get_delayed_failures()):
            step = failure['step']
            location = failure['location']
            message = failure['message']
            to_string = dedent('''\
               --------------------
               Failure {index}

               {step}
               ({location})
               --------------------

               {message}
            ''').format(index=index + 1, **failure)
            result.append(to_string)
        return '\n\n'.join(result)


class JsonDelayedFailures(DelayedFailures):

    def __init__(self, context, filepath):
        super(JsonDelayedFailures, self).__init__(context)
        self._filepath = filepath

    def get_delayed_failures(self):
        with open(self.get_delayed_failures_filepath(), 'r') as fin:
            return json.load(fin)

    def save_delayed_failure(self, failure):
        update_json_file(self.get_delayed_failures_filepath(), [failure])

    def delayed_failures_exist(self):
        return os.path.exists(self.get_delayed_failures_filepath())

    def get_delayed_failures_filepath(self):
        return self._filepath


def update_json_file(filepath, obj, overwrite=False):
    if not isinstance(obj, (list, dict)):
        raise TypeError('obj must be a list or a dict')

    if not overwrite and os.path.exists(filepath):
        file_content = read_json_file(filepath)
        if not isinstance(obj, type(file_content)):
            raise TypeError('obj and current file content must be of the same type')
    else:
        file_content = type(obj)()

    if isinstance(file_content, dict):
        update_content = file_content.update
    else:
        assert isinstance(file_content, list)
        update_content = file_content.extend
    update_content(obj)
    write_json_file(filepath, file_content)


def write_json_file(filepath, obj):
    with open(filepath, 'w') as fout:
        json.dump(obj, fout, sort_keys=True, indent=4, cls=DecimalJSONEncoder)


def read_json_file(filepath):
    with open(filepath, 'r') as fin:
        return json.load(fin)


class DecimalJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        else:
            return super(DecimalJSONEncoder, self).default(obj)
