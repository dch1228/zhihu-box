# coding=utf-8
import traceback

import requests
from bs4 import BeautifulSoup

from ext import Ext
from config import ZHIHU_USER, ZHIHU_PASSWORD

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


def get_xsrf():
    url = 'https://www.zhihu.com/'

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup.find('input', {'name': '_xsrf'}).get('value')


def login():
    url = 'https://www.zhihu.com/login/email'
    email = ZHIHU_USER
    password = ZHIHU_PASSWORD

    form_data = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf()
    }

    Ext.zhihu_session = requests.Session()

    resp = Ext.zhihu_session.post(url, headers=headers, data=form_data)
    if resp.status_code == 200:
        print(u'登录成功.')
        return

    print(u'登录失败')


def get_user_info():
    url = 'https://www.zhihu.com/people/du-chen-hao-13/activities'

    r = Ext.zhihu_session.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    like_count = soup.find('div', {'class': 'IconGraf'}).get_text().split()[1]
    following_count = soup.find('div', {'class': 'NumberBoard-value'}).get_text()
    follower_count = soup.find_all('div', {'class': 'NumberBoard-value'})[1].get_text()

    profile_light_item = soup.find_all('span', {'class': 'Profile-lightItemValue'})

    topics_count = profile_light_item[0].get_text()
    columns_count = profile_light_item[1].get_text()
    questions_count = profile_light_item[2].get_text()
    collections_count = profile_light_item[3].get_text()

    views_count = soup.find('div', {'class': 'Profile-footerOperations'}).get_text().split()[1]

    return {
        'like_count': int(like_count),
        'following_count': int(following_count),
        'follower_count': int(follower_count),
        'topics_count': int(topics_count),
        'columns_count': int(columns_count),
        'questions_count': int(questions_count),
        'collections_count': int(collections_count),
        'views_count': int(views_count),
    }


def get_news():
    url = 'https://www.zhihu.com/'

    r = Ext.zhihu_session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    items = soup.find_all('div', {'class': 'feed-item-inner'})

    res = []

    for item in items:
        try:
            res.append({
                'title': item.find('div', {'class': 'feed-source'}).get_text(),
                'content': item.find('h2', {'class': 'feed-title'}).get_text(),
                'href': item.find('h2', {'class': 'feed-title'}).find('a').get('href'),
                'avatar': item.find('div', {'class': 'avatar'}).find('img').get('src').split('/')[-1]
            })
        except:
            traceback.print_exc()

    return res
