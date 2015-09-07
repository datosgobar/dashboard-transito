#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import logging
import logging.config


class dashboard_logging(object):

    def __init__(self, config, name):
        self.logger = logging.getLogger(name)
        self.__default_path = config
        self.__setup_logging()

    def __setup_logging(self, env_key='LOG_CFG'):
        """Setup logging configuration

        """
        path = self.__default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=logging.INFO)

    def debug(self, debug):
        self.logger.debug('%s', debug)

    def info(self, info):
        self.logger.info('%s', info)

    def warning(self, warning):
        self.logger.warning('%s', warning)

    def error(self, error, traceback=False):
        self.logger.error('%s', error, exc_info=traceback)

    def critical(self, critical):
        self.logger.error('%s', critical)


if __name__ == '__main__':
    logger = dashboard_logging(config="logging.json", name=__name__)
    logger.info("alkjasdl")
    alsdkjasd = 'asdasd'
    try:
        print alsdkjasd + 1
    except Exception, e:
        logger.error('Failed to open file', traceback=True)
