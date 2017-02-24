import StringIO

from flask import Blueprint, render_template, send_file
import requests

import models
from spider import parser

bp = Blueprint('core', __name__, url_prefix='')


@bp.route('/zhihu_avatar/<link>')
def zhihu_avatar(link):
    str_io = StringIO.StringIO()

    r = requests.get('https://pic2.zhimg.com/{}'.format(link))

    str_io.write(r.content)

    str_io.seek(0)
    return send_file(str_io, mimetype='image/jpeg')


@bp.route('/')
def index():
    user_info = models.get_user_info()
    return render_template('dashboard.html', **locals())


@bp.route('/articles')
def articles():
    articles_list = [
        {
            'title': 'title',
            'author': 'author',
            'release_time': '0000-00-00',
            'like_count': 100,
            'comment_count': 20,
            'href': 'xx'
        }
    ]
    return render_template('articles.html', **locals())


@bp.route('/following')
def following():
    return render_template('following.html')


@bp.route('/news')
def news():
    items = models.get_news()
    return render_template('news.html', **locals())
