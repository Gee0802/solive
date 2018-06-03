from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Regexp
from werkzeug.datastructures import FileStorage

from ..models import User


class InfoForm(FlaskForm):
    avatar = FileField()
    nickname = StringField('昵称', validators=[DataRequired(),
                                             Regexp(r'[\u4e00-\u9fa5a-zA-Z_\d]+$', 0, message='昵称包含非法字符！')])
    submit_info = SubmitField('保存修改')

    def validate_avatar(self, field):
        if field.data != '' and  not isinstance(field.data, FileStorage):
            raise ValidationError('不合法的输入！')
        elif isinstance(field.data, FileStorage) and\
                not field.data.filename.endswith(current_app.config['ALLOWED_UPLOAD_TYPES']):
            raise ValidationError('不支持的上传格式！')

    def validate_nickname(self, field):
        if field.data == current_user.nickname:
            return
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在！')


class PasswordForm(FlaskForm):
    old_pw = PasswordField('请输入旧密码', validators=[DataRequired()])
    new_pw = PasswordField('请输入新密码', validators=[DataRequired(), Length(8, 16)])
    new_pw2 = PasswordField('请再次输入新密码', validators=[DataRequired(), EqualTo('new_pw', message='两次输入不一致！')])
    submit_pw = SubmitField('保存修改')

    def validate_old_pw(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('密码输入错误！')