#!/usr/bin/env python
# -*- coding: utf8 -*-
"""ip proxy parser"""

__author__ = 'feix.zhou'


import re
import BeautifulSoup

from parser import Parser

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Base(object):

    enable = False
    encoding = ''

    @classmethod
    def url_constructor(cls, keyword):
        return NotImplemented

    @classmethod
    def search_handler(cls, keyword, text):
        return NotImplemented

    @classmethod
    def result_handler(cls, keyword, result):
        return NotImplemente

    @classmethod
    def crawl(cls):
        keywords = [cls.__name__.lower()]
        parser = Parser(protocol=cls.site.split(':')[0], referer=cls.site, encoding=cls.encoding)
        results = parser.start(keywords=keywords,
                               url_constructor=cls.url_constructor,
                               search_handler=cls.search_handler,
                               result_handler=cls.result_handler)
        # print parser.time()
        return results


class CZ88(Base):

    enable = True
    site = 'http://www.cz88.net'
    encoding = 'gbk'

    @classmethod
    def url_constructor(cls, keyword):
        url_base = '{site}/proxy/{page}'
        pages = ['index.shtml']
        pages.extend(['http_{index}.shtml'.format(index=index) for index in range(2, 11)])
        for page in pages:
            yield (keyword, url_base.format(site=cls.site, page=page))

    @classmethod
    def search_handler(cls, keyword, text):
        results = []
        soup = BeautifulSoup.BeautifulSoup(text)
        proxy_list = soup.find('div', attrs={'class': 'box694'})
        if not proxy_list:
            return results
        proxy_list = proxy_list.findAll('li')
        for proxy in proxy_list:
            contents = [div.text for div in proxy.findAll('div')]
            if not contents or contents[0] == 'IP':
                continue
            keys = ['ip', 'port']
            results.append(dict(zip(keys, contents[:2])))
        return results

    @classmethod
    def result_handler(cls, keyword, result):
        return result['ip'], result['port']


class KuaiDaiLi(Base):

    enable = True
    site = 'http://blog.kuaidaili.com'

    @classmethod
    def url_constructor(cls, keyword):
        yield (keyword, cls.site)

    @classmethod
    def search_handler(cls, keyword, text):
        soup = BeautifulSoup.BeautifulSoup(text)
        blog_list = soup.findAll('article')
        results = []
        for blog in blog_list:
            url = blog.find('a').get('href')
            results.append({'url': url,
                            'request': 'url',
                            'redirect': True,
                            'multi': True})
        return results

    @classmethod
    def result_handler(cls, keyword, result):
        soup = BeautifulSoup.BeautifulSoup(result['result'])
        contents = soup.find('div', attrs={'class': 'entry-content'}).findAll('p')[1]
        for content in contents.contents:
            if not content or str(content) == '<br />':
                continue
            content = re.split('&nbsp;&nbsp;|:', content.strip())[:2]
            yield content[0], content[1]


class KuaiDaiLi2(Base):

    enable = True
    site = 'http://www.kuaidaili.com'

    @classmethod
    def url_constructor(cls, keyword):
        url_base = '{site}/proxylist/{index}'
        for index in range(1, 11):
            yield (keyword, url_base.format(site=cls.site, index=index))

    @classmethod
    def search_handler(cls, keyword, text):
        results = []
        soup = BeautifulSoup.BeautifulSoup(text)
        proxy_list = soup.find('tbody')
        if not proxy_list:
            return results
        proxy_list = proxy_list.findAll('tr')
        for proxy in proxy_list:
            contents = [td.text for td in proxy.findAll('td')]
            results.append({'ip': contents[0],
                            'port': contents[1]})
        return results

    @classmethod
    def result_handler(cls, keyword, result):
        return result['ip'], result['port']


class XiCiDaiLi(Base):

    site = 'http://www.xicidaili.com'

    @classmethod
    def url_constructor(cls, keyword):
        url_base = '{site}/{page}/{index}'
        pages = {'nn': 900,
                 'nt': 400,
                 'wn': 250,
                 'wt': 550}
        for page in pages:
            for index in range(1, pages[page]):
                yield (keyword, url_base.format(site=cls.site, page=page, index=index))

    @classmethod
    def search_handler(cls, keyword, text):
        return []

    @classmethod
    def result_handler(cls, keyword, result):
        return []


class IP66(Base):

    site = 'http://www.66ip.cn'

    @classmethod
    def url_constructor(cls, keyword):
        url_base = '{site}/{index}.html'
        for index in range(1, 500):
            yield (keyword, url_base.format(site=cls.site, index=index))

    @classmethod
    def search_handler(cls, keyword, text):
        return []

    @classmethod
    def result_handler(cls, keyword, result):
        return []


class IP66API(Base):

    site = 'http://www.66ip.cn'

    @classmethod
    def url_constructor(cls, keyword):
        url_base = '{site}/{page}'
        pages = ['mo.php?tqsl=800', 'nmtq.php?getnum=800&anonymoustype=4&proxytype=2&api=66ip']
        pages.extend('nmtq.php?getnum=800&anonymoustype={proxy_type}&proxytype=2&api=66ip'.format(proxy_type=proxy_type) for proxy_type in range(1, 4))
        for page in pages:
            yield (keyword, url_base.format(site=cls.site, page=page))

    @classmethod
    def search_handler(cls, keyword, text):
        return []

    @classmethod
    def result_handler(cls, keyword, result):
        return []


def test():
    for cls in Base.__subclasses__():
        print cls.__name__
        keyword = cls.__name__.lower()
        print list(cls.url_constructor(keyword))


def main():
    with open('proxy.txt', 'a') as f:
        for cls in Base.__subclasses__():
            if cls.enable:
                print cls.__name__
                for proxy in cls.crawl():
                    f.write('{}{}'.format(':'.join(proxy), '\n'))


if __name__ == '__main__':
    main()
