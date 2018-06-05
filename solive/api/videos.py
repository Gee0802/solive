from flask import request, jsonify
from flask import current_app as app

from . import api
from ..models import Video
from ..exts import db


@api.route('/videos/hosts')
def get_hosts():
    args = request.args
    if args['source'] == '全部':
        clause1 = True
    else:
        clause1 = (Video.source == app.config['SOURCE_URL_MAPPINGS'][args['source']])
    if args['cate'] == '全部':
        clause2 = True
    else:
        clause2 = (Video.cate == args['cate'])
    videos = Video.query.filter(db.and_(clause1, clause2)).filter(Video.latest(Video, app.config['SO_TIME'])) \
                 .order_by(Video.viewers_num.desc())[:12]
    required_data = ['nickname', 'room', 'cate', 'source', 'is_live']
    return jsonify({
        'code': '200',
        'message': 'success',
        'data': [{k: v for k, v in video.to_json().items() if k in required_data} for video in videos]
    })


@api.route('/videos')
def get_videos():
    args =  request.args
    videos = Video.query.filter((Video.cate == args['cate']) | (Video.parent_cate_name == args['cate']))\
                .filter(Video.latest(Video, app.config['SO_TIME'])).order_by(Video.viewers_num.desc())[:8]
    return jsonify({
        'code': '200',
        'message': 'success',
        'data': [video.to_json() for video in videos]
    })
