from flask import Blueprint
from jinja2.runtime import Undefined


main = Blueprint('main', __name__)


def f(s):
    if isinstance(s, Undefined):
        return ''
    return s + '_'

main.add_app_template_filter(f)


from . import views