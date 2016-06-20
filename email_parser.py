#!/usr/bin/env python
# -*- coding: utf8 -*-
""" email """

__author__ = 'feix.chow'

import re
import BeautifulSoup

from parser import Parser

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def google_search_handler(keyword, text):
    soup = BeautifulSoup.BeautifulSoup(text)
    contents = soup.findAll('h3', attrs={'class': 'r'})
    results = []
    for content in contents:
        url = content.find('a').get('href')
        results.append({'url': url,
                        'request': 'url',
                        'redirect': True})
    return results


def baidu_search_handler(keyword, text):
    soup = BeautifulSoup.BeautifulSoup(text)
    results = []
    contents = soup.findAll('div', attrs={'class': 'result c-container '})
    for content in contents:
        content = content.find('a')
        url = content.get('href')
        results.append({'url': url,
                        'request': 'url',
                        'redirect': True})
    return results


def sogou_search_handler(keyword, text):
    soup = BeautifulSoup.BeautifulSoup(text)
    contents = soup.findAll('div', attrs={'class': 'rb'})
    results = []
    for content in contents:
        url = content.find('a').get('href')
        results.append({'url': url,
                        'request': 'url',
                        'redirect': True})
    return results


def result_handler(keyword, result):
    reg_emails = re.compile(
        # Local part is required, charset is flexible
        # https://tools.ietf.org/html/rfc6531 (removed * and () as they provide FP mostly )
        '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' +
        '@' +
        '[a-zA-Z0-9.-]*' + keyword)
    print reg_emails
    return set(reg_emails.findall(result['result']))


def main():
    import sys
    keywords = sys.argv[1:]
    # baidu_parser = Parser(protocol='http', referer='http://www.baidu.com/')
    # search_handler = baidu_search_handler
    # from url_constructor import baidu_url_constructor as url_constructor
    # results = baidu_parser.start(keywords=keywords, url_constructor=url_constructor, search_handler=search_handler, result_handler=result_handler)
    sogou_parser = Parser(protocol='https', referer='https://www.sogou.com/')
    search_handler = sogou_search_handler
    from url_constructor import sogou_url_constructor as url_constructor
    results = sogou_parser.start(keywords=keywords, url_constructor=url_constructor, search_handler=search_handler, result_handler=result_handler)
    print set(results)


if __name__ == '__main__':
    main()
