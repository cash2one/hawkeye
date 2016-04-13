#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'feix.chow'


import hashlib
import BeautifulSoup
from collections import defaultdict

from parser import Parser
from url_constructor import github_url_constructor as url_constructor


def search_handler(keyword, text):
    soup = BeautifulSoup.BeautifulSoup(text)
    code_list = soup.findAll('div', attrs={'class': 'code-list-item code-list-item-public '})
    results = []
    for code in code_list:
        urls = code.findAll('a')
        project_url = urls[1].get('href')
        file_url = urls[2].get('href')
        if not project_url or not file_url:
            continue
        if file_url.split('.')[-1] in ('jpg', 'css', 'html', 'gif', 'svg'):
            continue
        if len(file_url) >= 235:
            continue
        if project_url and file_url and (project_url, file_url) not in results:
            results.append({'file': 'https://raw.githubusercontent.com' + file_url.replace('/blob/', '/'),
                            'project_url': project_url,
                            'file_url': 'https://github.com' + file_url,
                            'timeout': 10,
                            'request': 'file',
                            'redirect': False})
    return results


def result_handler(keyword, result):
    if result['result']:
        result_md5 = hashlib.md5(result['result'].encode('utf-8'))
        result_md5 = result_md5.hexdigest()
        return keyword, result_md5, result['file_url']


def main():
    parser = Parser(protocol='https', referer='https://github.com')
    keywords = ['feix.chow parser']
    results = parser.start(keywords=keywords, url_constructor=url_constructor, search_handler=search_handler, result_handler=result_handler)
    print results
    print parser.time()


if __name__ == '__main__':
    main()
