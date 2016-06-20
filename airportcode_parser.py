#!/usr/bin/env python
# -*- coding: utf8 -*-
""" airportcode """

__author__ = 'feix.chow'

import BeautifulSoup

from parser import Parser

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def url_constructor(keyword):
    url_base = 'http://airportcode.911cha.com/list_{index}.html'
    for index in range(0, 300):
        yield (keyword, url_base.format(index=index))


def search_handler(keyword, text):
    results = []
    soup = BeautifulSoup.BeautifulSoup(text)
    contents = soup.find('tbody')
    if not contents:
        return results
    contents = contents.findAll('tr')
    for content in contents:
        codes = [td.text for td in content.findAll('td')]
        if not codes or len(codes) < 5:
            continue
        keys = ['city', 'tcode', 'fcode', 'airport_cn', 'airport']
        results.append(dict(zip(keys, codes)))
    return results


def result_handler(keyword, result):
    return result['city'], result['tcode'], result['fcode'], result['airport_cn'], result['airport']


def test():
    for item in search_handler(sys.stdin):
        for key, value in item.items():
            print key, value


def main():
    keywords = ['airportcode']
    parser = Parser(protocol='http', referer='http://airportcode.911cha.com')
    results = parser.start(keywords=keywords, url_constructor=url_constructor, search_handler=search_handler, result_handler=result_handler)
    print results
    print parser.time()


if __name__ == '__main__':
    main()
