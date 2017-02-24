import json

from ext import Ext
from spider import parser


def save_user_info(d):
    Ext.cache.set('user_info', json.dumps(d))


def get_user_info():
    user_info = Ext.cache.get('user_info')

    if not user_info:
        Ext.zhihu_session or parser.login()
        user_info = parser.get_user_info()
        save_user_info(user_info)
    else:
        user_info = json.loads(user_info)

    return user_info


def save_news(d):
    Ext.cache.set('news', json.dumps(d))


def get_news():
    news = Ext.cache.get('news')

    if not news:
        Ext.zhihu_session or parser.login()
        news = parser.get_news()
        save_news(news)
    else:
        news = json.loads(news)

    return news


def refresh_news():
    Ext.zhihu_session or parser.login()

    news = parser.get_news()
    save_news(news)
    return news


def refresh_user_info():
    Ext.zhihu_session or parser.login()

    user_info = parser.get_user_info()
    save_user_info(user_info)
    return user_info
