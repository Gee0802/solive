from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_login import login_required, current_user
from pyecharts import Bar
import datetime
import random
import json

from . import main
from .url_cate_mappings import url_cate_mappings, cate_url_mappings, hot_hosts, so_labels, SO_TIME, \
    source_index_mappings, url_source_mappings
from ..exts import db
from ..models import User, Video, Category


@main.route('/')
def index():
    # 轮播数据
    carousel = Video.query.filter(Video.latest(Video, SO_TIME)).order_by(Video.viewers_num.desc())[:5]

    # 各个直播平台直播间个数
    lives_num_list = sorted(json.load(open('live_crawler/live.json')), key=lambda x: x['lives_num'], reverse=True)

    # so主播数据
    host_sample = random.sample(hot_hosts, 12)
    hosts = []
    for room in host_sample:
        host = Video.query.filter(Video.room == room).first()
        if host is not None:
            if host.latest(host, 300):
                hosts.append((host, True))
            else:
                hosts.append((host, False))

    # so游戏、so娱乐数据
    render_so = {}
    render_so['game'] = Video.query.filter(Video.latest(Video, SO_TIME)) \
                            .filter(Video.cate.in_(so_labels['game'])).order_by(Video.viewers_num.desc())[:8]
    render_so['entertainment'] = Video.query.filter(Video.latest(Video, SO_TIME)) \
                            .filter(Video.cate.in_(so_labels['entertainment'])).order_by(Video.viewers_num.desc())[:8]
    return render_template('index.html', carousel=carousel, lives_num_list=lives_num_list,
                           source_index_mappings=source_index_mappings, url_source_mappings=url_source_mappings,
                           hosts=hosts, render_so=render_so, so_labels=so_labels)


@main.route('/chart')
def chart():
    data = {
        '张三': 123.3,
        '李四': 66.8,
        '王五': 86.4,
        '杨六': 77.9,
        'ji': 46.3,
        'pp': 110.4
    }
    bar = Bar()
    v1, v2 = bar.cast(data)
    bar.add('weight', v1, v2)
    return render_template('simple_chart.html', chart=bar)


@main.route('/all')
@main.route('/all/<int:page>')
def all(page=1):
    pagination = Video.query.filter(Video.latest(Video, SO_TIME)).order_by(Video.viewers_num.desc())\
        .paginate(page, 40, False)
    return render_template('all.html', title='全部直播', pagination=pagination)


@main.route('/cate')
def cate():
    # aggregation = {}
    # for v in mappings.values():
    #     res = Video.aggregate(v, SO_TIME)
    #     aggregation[v] = [res.total_room, res.total_num]
    aggregation = Video.aggregate(time_delta=SO_TIME)
    # TODO: 按照cate_url_mappings来排序：遍历aggregation，mappings[name] = item.
    return render_template('cate.html', title='全部分类', mappings=cate_url_mappings, aggregation=aggregation)


@main.route('/cate/<string:name>')
@main.route('/cate/<string:name>/<int:page>')
def show_cate(name, page=1):
    if name not in url_cate_mappings:
        flash('您访问的页面不存在！')
        return redirect(request.referrer or url_for('.cate'))
    # cate = Category.query.filter_by(name=mappings[name]).first()
    # if cate is None:
    #     flash('您访问的页面不存在！')
    #     return redirect(request.referrer or url_for('.cate'))
    # pagination = cate.contains.paginate(1, 40, False)
    videos = Video.query.filter_by(parent_cate_name=url_cate_mappings[name]).filter(Video.latest(Video, SO_TIME))\
        .order_by(Video.viewers_num.desc())
    pagination = videos.paginate(page, 40, False)
    # res = videos.group_by(Video.parent_cate_name)
    return render_template('all.html', title=url_cate_mappings[name], pagination=pagination)


@main.route('/search')
def search():
    keyword = request.args.get('keyword')
    if keyword is not None:
        videos = Video.query.filter(db.or_(Video.title.like('%{}%'.format(keyword)), Video.nickname.like('%{}%'.format(keyword))))\
            .order_by(Video.viewers_num.desc())
        if videos is not None:
            page = int(request.args.get('page') or 1)
            pagination = videos.paginate(page, 40, False)
            return render_template('search.html', title=keyword, pagination=pagination)
    return abort(404)   # TODO


@main.route('/user/history')
@login_required
def user_history():
    if current_user.is_authenticated:
        pagination = current_user.history.paginate(1, 40, False)
        return render_template('history.html', title='观看历史', pagination=pagination)
        # TODO


@main.route('/user/favorite')
@login_required
def user_favorite():
    if current_user.is_authenticated:
        pagination = current_user.favorite.paginate(1, 40, False)
        return render_template('favorite.html', title='我的收藏', pagination=pagination)


@main.route('/favorite', methods=['GET', 'POST'])
@login_required
def favorite():
    data = request.form
    video = current_user.favorite.filter(Video.room == data['video']).first()
    if data['operation'] == '添加收藏':
        if video is None:
            video = Video.query.filter(Video.room == data['video']).first()
            current_user.favorite.append(video)
            operation = '取消收藏'
            return jsonify({'operation': operation})
        error_message = '您已收藏这个房间，请勿重复添加！'
    elif data['operation'] == '取消收藏':
        if video:
            current_user.favorite.remove(video)
            operation = '添加收藏'
            return jsonify({'operation': operation})
        error_message = '您尚未收藏此房间，取消收藏失败！'
    return jsonify({'message': error_message}), 400


@main.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    data = request.form
    video = Video.query.filter(Video.room == data['video']).first()
    if video is not None:
        if video not in current_user.history:
            current_user.history.append(video)
    return jsonify({})
