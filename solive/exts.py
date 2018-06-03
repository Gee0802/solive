"""
 This module is intended for some extensions which may cause circular references.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'