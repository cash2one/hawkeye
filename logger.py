# -*- coding: utf8 -*-

__author__ = 'feix.chow'


import logging


logging.basicConfig(filename='parser.log',
                    filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logging.info('hello')
