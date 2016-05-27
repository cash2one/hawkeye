# -*- coding: utf8 -*-

__author__ = 'feix.chow'


def github_url_constructor(keyword, indexs=101):
    url_base = 'https://github.com/search?p={index}&q={keyword}&type=Code&utf8=%E2%9C%93'
    for index in range(1, indexs):
        yield (keyword, url_base.format(index=index, keyword=keyword))


def baidu_url_constructor(keyword, indexs=50):
    url_base = 'http://www.baidu.com/s?pn={index}&wd={keyword}'
    for index in range(0, indexs):
        yield (keyword, url_base.format(index=index * 10, keyword=keyword))


def google_url_constructor(keyword, indexs=50):
    url_base = 'https://www.google.com/search?num=50&start={index}&q={keyword}'
    for index in range(0, indexs):
        yield (keyword, url_base.format(index=index, keyword=keyword))


def sogou_url_constructor(keyword, indexs=50):
    url_base = 'https://www.sogou.com/web?page={index}&query={keyword}'
    for index in range(0, indexs):
        yield (keyword, url_base.format(index=index, keyword=keyword))
