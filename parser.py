# -*- coding: utf8 -*-

__author__ = 'feix.chow'


import time
import random
import requests
from multiprocessing.dummy import Pool as threadPool

from proxy import Proxy
from logger import logging


_user_agents = ['Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)']


class Parser(object):

    def __init__(self, Proxy=Proxy, protocol='http', referer='', user_agents=_user_agents, encoding=''):
        self.proxies = list(Proxy().get_proxies())
        self.user_agents = list(user_agents)
        self.protocol = protocol
        self.referer = referer
        self.encoding = encoding
        self.search_handler = None
        self.result_handler = None
        self.start_time = None
        self.end_time = None

    def start(self, keywords, url_constructor, thread_num=10, search_handler=lambda k, t: [{'result': t}], result_handler=lambda k, t: (k, t)):
        self.start_time = time.time()
        self.search_handler = search_handler
        self.result_handler = result_handler
        keyword_urls = []
        results = []
        logging.info('Parser start')
        for keyword in keywords:
            keyword_urls.extend(url_constructor(keyword))
            logging.info('Construct url with {}'.format(keyword))
        logging.info('Start {} thread'.format(thread_num))
        pool = threadPool(thread_num)
        # multi thread debug
        # [results.extend(r) for r in map(self.request, keyword_urls) if r]
        [results.extend(r) for r in pool.map(self.request, keyword_urls) if r]
        logging.info('End all thread')
        pool.close()
        pool.join
        self.end_time = time.time()
        logging.info('Spend time {}'.format(self.time()))
        return filter(lambda t: bool(t), results)

    def time(self):
        return self.end_time - self.start_time

    def request(self, keyword_url):
        if not self.proxies:
            logging.error('No proxy is available')
            return None
        referer = self.referer
        proxy = random.choice(self.proxies)
        user_agent = random.choice(self.user_agents)
        proxies = {self.protocol: '{}://{}'.format(self.protocol, proxy)}
        headers = {'User-Agent': user_agent, 'referer': referer}
        keyword = keyword_url[0]
        url = keyword_url[1]
        timeout = 10
        try:
            req = requests.get(url, proxies=proxies, headers=headers, timeout=timeout)
        except Exception, e:
            # print e
            # remove useless proxy
            try:
                self.proxies.remove(proxy)
                logging.INFO('Remove userless proxy {}'.format(proxy))
            except:
                pass
            return self.request(keyword_url)
        if req.ok:
            if self.encoding:
                req.encoding = self.encoding
            search_results = self.search_handler(keyword, req.text)
            results = []
            for result in search_results:
                request = result.get('request', None)
                if request:
                    headers['referer'] = url
                    url = result.get(request)
                    timeout = result.get('timeout')
                    result['result'] = result.get('result', None)
                    try:
                        req = requests.get(url, proxies=proxies, headers=headers, timeout=timeout, allow_redirects=result['redirect'])
                        if req.ok:
                            if result.get('encoding'):
                                req.encoding = result.get('encoding')
                            elif self.encoding:
                                req.encoding = self.encoding
                            result['result'] = req.text
                            if result['redirect']:
                                result[request] = req.url
                    except Exception, e:
                        logging.INFO('Request result {} error'.format(url))
                        # print e
                        pass
                if result.get('multi'):
                    results.extend(self.result_handler(keyword, result))
                else:
                    results.append(self.result_handler(keyword, result))
            return results
