# -*- coding: utf8 -*-

__author__ = 'feix.chow'


def github_url_constructor(keyword, indexs=101):
    url_base = 'https://github.com/search?p={index}&q={keyword}&type=Code&utf8=%E2%9C%93'
    for index in range(1, indexs):
        yield (keyword, url_base.format(index=index, keyword=keyword))


def baidu_url_constructor(keyword, indexs=50):
    url_base = 'http://www.baidu.com/s?pn={index}&wd={keyword}'
    for index in range(0, index):
        yield (keyword, url_base.format(index=index * 10, keyword=keyword))
