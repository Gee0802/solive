from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_login import login_required, current_user
from pyecharts import Bar
import random
import json

from . import main
from config import SO_TIME, HOT_HOSTS, URL_CATE_MAPPINGS, CATE_URL_MAPPINGS, SO_LABELS
from ..exts import db
from ..models import Video


@main.route('/')
def index():
    # 轮播数据
    carousel = Video.query.filter(Video.latest(Video, SO_TIME)).order_by(Video.viewers_num.desc())[:5]

    # 各个直播平台直播间个数
    with open('live_crawler/live.json') as f:
        lives_num_list = sorted(json.load(f), key=lambda x: x['lives_num'], reverse=True)

    # so主播数据
    host_sample = random.sample(HOT_HOSTS, 12)
    hosts = []
    for room in host_sample:
        host = Video.query.filter(Video.room == room).first()
        if host is not None:
            if host.latest(host, SO_TIME):
                hosts.append((host, True))
            else:
                hosts.append((host, False))

    # so游戏、so娱乐数据
    render_so = {}
    render_so['game'] = Video.query.filter(Video.latest(Video, SO_TIME)) \
                            .filter(Video.cate.in_(SO_LABELS['game'])).order_by(Video.viewers_num.desc())[:8]
    render_so['entertainment'] = Video.query.filter(Video.latest(Video, SO_TIME)) \
                            .filter(Video.cate.in_(SO_LABELS['entertainment'])).order_by(Video.viewers_num.desc())[:8]
    return render_template('index.html', carousel=carousel, lives_num_list=lives_num_list, hosts=hosts,
                           render_so=render_so)


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
    return render_template('cate.html', title='全部分类', mappings=CATE_URL_MAPPINGS, aggregation=aggregation)


@main.route('/cate/<string:name>')
@main.route('/cate/<string:name>/<int:page>')
def show_cate(name, page=1):
    if name not in URL_CATE_MAPPINGS:
        flash('您访问的页面不存在！')
        return redirect(request.referrer or url_for('.cate'))
    videos = Video.query.filter_by(parent_cate_name=URL_CATE_MAPPINGS[name]).filter(Video.latest(Video, SO_TIME))\
        .order_by(Video.viewers_num.desc())
    pagination = videos.paginate(page, 40, False)
    return render_template('all.html', title=URL_CATE_MAPPINGS[name], pagination=pagination)


@main.route('/search')
def search():
    keyword = request.args.get('keyword')
    if keyword is not None:
        videos = Video.query.filter(db.or_(Video.title.like('%{}%'.format(keyword)),
                                           Video.nickname.like('%{}%'.format(keyword))))\
            .order_by(Video.viewers_num.desc())
        if videos is not None:
            page = int(request.args.get('page') or 1)
            pagination = videos.paginate(page, 40, False)
            return render_template('search.html', title=keyword, pagination=pagination)
    return abort(404)   # TODO


@main.route('/favorite', methods=['POST'])
def favorite():
    if current_user.is_authenticated:
        data = request.form
        video = current_user.favorite.filter(Video.room == data['video']).first()
        if data['operation'] == '添加收藏':
            if video is None:
                video = Video.query.filter(Video.room == data['video']).first()
                current_user.favorite.append(video)
                operation = '取消收藏'
                return jsonify({'code': '200', 'operation': operation})
            error_message = '您已收藏这个房间，请勿重复添加！'
        elif data['operation'] == '取消收藏':
            if video is not None:
                current_user.favorite.remove(video)
                operation = '添加收藏'
                return jsonify({'code': '200', 'operation': operation})
            error_message = '您尚未收藏此房间，取消收藏失败！'
        else:
            error_message = '未知的操作！'
        return jsonify({'code': '400', 'message': error_message})
    error_message = '请登录！'
    return jsonify({'code': '401', 'message': error_message})


@main.route('/history', methods=['POST'])
def history():
    if current_user.is_authenticated:
        data = request.form
        video = Video.query.filter(Video.room == data['video']).first()
        if video is not None:
            if video not in current_user.history:
                current_user.history.append(video)
    return jsonify({})
