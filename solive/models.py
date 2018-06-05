from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime

from .exts import db, login_manager
from config import SO_TIME


favorites = db.Table('favorites',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('video_id', db.Integer, db.ForeignKey('videos.id')))


histories = db.Table('histories',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('video_id', db.Integer, db.ForeignKey('videos.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64))
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(64), default='default.jpg')
    experience = db.Column(db.Integer, server_default=db.text('0'))
    last_seen = db.Column(db.DateTime())
    favorite = db.relationship('Video', secondary='favorites', lazy='dynamic')
    history = db.relationship('Video', secondary='histories', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def level(self):
        import math
        return int(math.sqrt(self.experience + 1))

    @property
    def exp_to_level_up(self):
        return self.level * 2 + 1

    @property
    def current_level_exp(self):
        return self.experience - self.level ** 2 + 1

    def add_exp(self, increment=1):
        self.experience += increment

    def first_seen_today(self):
        if self.last_seen is not None:
            return self.last_seen.date() != datetime.datetime.now().date()
        return True

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Video(db.Model):
    __tablename__ = 'videos'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    source = db.Column(db.String(32))
    nickname = db.Column(db.String(32))
    room = db.Column(db.String(128), unique=True)
    title = db.Column(db.String(128))
    cover = db.Column(db.String(256))
    viewers_num = db.Column(db.Integer)
    cate = db.Column(db.String(32))
    parent_cate_name = db.Column(db.String(32), db.ForeignKey('categories.name'))

    @staticmethod
    def latest(obj, time_delta=SO_TIME):
        """
        如果obj为类对象，该方法将返回一个SQL clause（没有定义常规的__bool__方法，因此bool（返回值）会报错：
        "Boolean value of this clause is not defined."），而不是一个逻辑表达式;
        如果obj为实例对象，该方法返回正常的逻辑表达式.
        :param obj: class or instance.
        :param time_delta: an integer minutes count.
        :return: True if 'Video.created' is less than 'time_delta' minutes earlier from now, else False.
        """
        if isinstance(time_delta, int):
            time_delta = datetime.timedelta(minutes=time_delta)
        else:
            raise TypeError('need an int argument but given %s' % type(time_delta))
        return obj.created > datetime.datetime.now() - time_delta

    def to_json(self):
        return {
            'nickname': self.nickname,
            'title': self.title,
            'room': self.room,
            'cover': self.cover,
            'source': self.source,
            'viewers_num': self.viewers_num,
            'created': self.created,
            'cate': self.cate,
            'parent_cate_name': self.parent_cate_name,
            'is_live': self.latest(self, SO_TIME)
        }

    @staticmethod
    def aggregate(cate=None, time_delta=SO_TIME):
        if cate is None:
            subquery = db.session.query(Video.parent_cate_name, db.func.count('*').label('total_room'),
                                      db.func.sum(Video.viewers_num).label('total_num'))\
                .filter(Video.latest(Video, time_delta)).group_by(Video.parent_cate_name).subquery()  # 将query对象转化为类Table对象
            result = db.session.query(subquery).order_by(subquery.c.total_num.desc())
        else:
            result = db.session.query(db.func.count('*').label('total_room'),
                                      db.func.sum(Video.viewers_num).label('total_num'))\
                .filter(Video.latest(Video, time_delta)).group_by(Video.parent_cate_name == cate)  # FIXME
        return result


class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    total_rooms = db.Column(db.Integer)
    total_viewers = db.Column(db.Integer)
    contains = db.relationship(Video, backref='parent_cate', lazy='dynamic')