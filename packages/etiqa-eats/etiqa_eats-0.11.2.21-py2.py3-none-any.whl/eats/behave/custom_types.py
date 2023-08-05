import behave
import parse
from ..users import Users

@parse.with_pattern(r'.*')
def possibly_empty(text):
    return text

@parse.with_pattern(r'I|\{[^\{\}]+\}')
def user_name(text):
    if text == 'I':
        return Users.DEFAULT_USERNAME
    else:
        return text.lstrip('{').rstrip('}')

#@parse.with_pattern(r's|es')
#def third_person_singular_verb_ending(text):
#    pass


def register_custom_types():
    behave.register_type(**{
        'PossiblyEmpty': possibly_empty,
        'Username': user_name,
    })