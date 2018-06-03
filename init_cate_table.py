from solive.models import Video, Category
from url_cate_mappings import mappings
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


config = dict(
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True,
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/test'
)

app = Flask(__name__)
app.config.from_mapping(config)
db = SQLAlchemy(app)
for name in mappings.values():
    cate = Category(name=name)
    db.session.add(cate)
    db.session.commit()


