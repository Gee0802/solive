from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from ..models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', render_kw={'placeholder': '邮箱/手机号'}, validators=[DataRequired('请输入用户名！')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码！')])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')

    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        user = User.query.filter(User.username == self.username.data).first()
        if user is None or not user.verify_password(self.password.data):
            try:
                raise ValidationError('用户名或密码错误！')
            except ValueError as e:
                self.password.errors.append(e.args[0])
            finally:
                return False
        return True


class RegisterForm(FlaskForm):
    username = StringField('用户名', render_kw={'placeholder': '邮箱/手机号'}, validators=[DataRequired()])
    nickname = StringField('昵称', validators=[DataRequired(), Regexp(r'[\u4e00-\u9fa5a-zA-Z_\d]+$', 0,
                                                                    message='昵称包含非法字符！')])
    password = PasswordField('设置密码', validators=[DataRequired(), Length(8, 16)])
    password2 = PasswordField('确认密码', validators=[EqualTo('password', message='两次输入密码不一致！')])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if field.data.isdigit():
            if len(field.data) != 11 or not field.data.startswith('1'):
                raise ValidationError('Invalid phone number.')
        else:
            Email()(self, field)
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在！')
