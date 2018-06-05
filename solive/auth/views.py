from flask import url_for, flash, redirect, request, jsonify
from flask_login import login_user, login_required, logout_user

from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User
from ..exts import db


@auth.app_context_processor
def add_forms():
    return dict(login_form=LoginForm(prefix='l'), register_form=RegisterForm(prefix='r'))


@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm(prefix='l')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, form.remember_me.data)
        return jsonify({'code': '200', 'message': 'success', 'data': {}})
    return jsonify({
        'code': '400',
        'message': 'error',
        'data': {form._prefix + k: v for k, v in form.errors.items()}
    })


@auth.route('/logout')
@login_required
def logout():
    print(request.referrer)
    logout_user()
    flash('您已退出登录！')
    return redirect(request.referrer or url_for('main.index'))


@auth.route('/register', methods=['POST'])
def register():
    form = RegisterForm(prefix='r')
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    nickname=form.nickname.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify({'code': '200', 'message': 'success', 'data': {}})
    return jsonify({
        'code': '400',
        'message': 'error',
        'data': {form._prefix + k: v for k, v in form.errors.items()}
    })
