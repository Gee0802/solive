from flask import abort, render_template, request, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename
import datetime

from . import user
from .forms import InfoForm, PasswordForm
from ..exts import db


@user.before_request
def before_user_request():
    if not current_user.is_authenticated:
        abort(401)


@user.before_app_request
def add_experience():
    if current_user.is_authenticated:
        if current_user.first_seen_today():
            current_user.add_exp()
        current_user.last_seen = datetime.datetime.now()


@user.route('/settings', methods=['GET', 'POST'])
def settings():
    info_form = InfoForm(meta={'csrf': False})
    password_form = PasswordForm(meta={'csrf': False})
    print(info_form.data)
    if not info_form.is_submitted():
        info_form.nickname.data = current_user.nickname
    elif info_form.validate_on_submit():
        file = request.files.get('avatar', None)
        if file:
            filename = '%s.%s' % (current_user.username, file.filename.rsplit('.', 1)[-1])
            file.save('solive/static/img/avatar/%s' % filename)
            current_user.avatar = filename
        current_user.nickname = info_form.nickname.data
        db.session.add(current_user)
        db.session.commit()
    return render_template('user/settings.html', info_form=info_form, password_form=password_form)


@user.route('/password', methods=['POST'])
def password():
    form = PasswordForm(meta={'csrf': False})
    if form.validate_on_submit():
        current_user.password = form.new_pw.data
        db.session.add(current_user)
        db.session.commit()
        return jsonify({'code': 200, 'message': 'success'})
    else:
        return jsonify({'code': 400, 'message': 'error', 'data': form.errors})


@user.route('/history')
def history():
    if current_user.is_authenticated:
        pagination = current_user.history.paginate(1, 40, False)
        return render_template('user/history.html', title='观看历史', pagination=pagination)
        # TODO


@user.route('/favorite')
def favorite():
    if current_user.is_authenticated:
        pagination = current_user.favorite.paginate(1, 40, False)
        return render_template('user/favorite.html', title='我的收藏', pagination=pagination)
