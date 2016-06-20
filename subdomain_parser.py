#!/usr/bin/env python
# -*- coding: utf8 -*-
""" subdomain """

__author__ = 'feix.chow'

import re
import BeautifulSoup

from parser import Parser

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def google_search_handler(keyword, text):
    soup = BeautifulSoup.BeautifulSoup(text)
    contents = soup.findAll('cite', attrs={'class': '_Rm'})
    results = []
    for content in contents:
        domain = content.contents[0].replace('/', '')
        results.append({'domain': domain})
    return results


def baidu_search_handler(keyword, text):
    soup = BeautifulSoup.BeautifulSoup(text)
    results = []
    contents = soup.findAll('div', attrs={'class': 'result c-container '})
    for content in contents:
        content = content.find('a', attrs={'class': 'c-showurl'})
        domain = content.contents[0].split('/')[0]
        domain = domain.replace('<em>', '').replace('</em>', '')
        results.append({'domain': domain})
    return results


def sogou_search_handler(keyword, text):
    soup = BeautifulSoup.BeautifulSoup(text)
    contents = soup.findAll('div', attrs={'class': 'r-sech site_query'})
    results = []
    for content in contents:
        domain = content.find('a').get('href').split('/')[2]
        results.append({'domain': domain})
    return results


def result_handler(keyword, result):
    return result['domain']


def main():
    import sys
    keywords = sys.argv[1:]
    keywords = ('site:' + keyword for keyword in keywords)
    sogou_parser = Parser(protocol='https', referer='https://www.sogou.com/')
    search_handler = sogou_search_handler
    from url_constructor import sogou_url_constructor as url_constructor
    results = sogou_parser.start(keywords=keywords, url_constructor=url_constructor, search_handler=search_handler, result_handler=result_handler)
    for result in set(results):
        print result


if __name__ == '__main__':
    main()
