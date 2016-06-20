#!/usr/bin/env python
# -*- coding: utf8 -*-
""" detect alive ip proxy """

__author__ = 'feix.chow'


import requests
from proxy import Proxy
from multiprocessing.dummy import Pool as threadPool


def detect_alive_proxy(proxy):
    url = 'http://www.baidu.com'
    timeout = 10
    proxies = {'http': 'http://{}'.format(proxy)}
    try:
        req = requests.get(url, proxies=proxies, timeout=timeout)
    except:
        return None
    if req.ok:
        return proxy


def main():
    pool = threadPool(20)
    proxies = Proxy().get_proxies()
    with open('proxy.txt', 'w') as f:
        for proxy in filter(bool, pool.map(detect_alive_proxy, proxies)):
            f.write(proxy + '\n')


if __name__ == '__main__':
    main()
