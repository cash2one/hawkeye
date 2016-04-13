# -*- coding: utf8 -*-

__author__ = 'feix.chow'


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Proxy(object):

    __metaclass__ = Singleton

    def __init__(self, proxy='proxy.txt'):
        self.proxies = set()
        with open(proxy) as f:
            for proxy in f:
                self.proxies.add(proxy.strip())

    def get_proxies(self, check_proxy=lambda t: True):
        for proxy in filter(check_proxy, self.proxies):
            yield proxy


if __name__ == '__main__':
    for proxy in Proxy().get_proxies():
        print proxy
