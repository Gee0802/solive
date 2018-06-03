from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
from pyecharts.conf import PyEchartsConfig
from pyecharts.engine import ECHAERTS_TEMPLATE_FUNCTIONS

from config import config
from .exts import db, login_manager
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .auth.forms import LoginForm, RegisterForm
from .api import api as api_blueprint
from .user import user as user_blueprint


# the dictionary of flask extension instances
ext_dict = dict(
    mail = Mail(),
    moment = Moment(),
    bootstrap = Bootstrap()
)
globals().update(ext_dict)

# Define the factory function of flask application.
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.jinja_env.globals.update(ECHAERTS_TEMPLATE_FUNCTIONS)
    app.jinja_env.pyecharts_config = PyEchartsConfig(jshost='https://cdn.bootcss.com/echarts/3.7.2')

    db.init_app(app)
    login_manager.init_app(app)

    for key in ext_dict:
        ext_dict[key].init_app(app)

    def add_template_globals():
        return app.config['GLOBAL_TEMPLATE_ARGS']
    app.context_processor(add_template_globals)

    return app


from . import models
