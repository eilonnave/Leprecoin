# -*- coding: utf-8 -*-
import logging
import os
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'


class Logger():
    def __init__(self, file_name):
        """
        constructor
        """
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        logging.basicConfig(format=LOG_FORMAT,
                            filename=LOG_DIR+'/'+file_name,
                            level=LOG_LEVEL)

    @staticmethod
    def info(message):
        """
        the function adds info message to the
        logging
        :param message: the message to logging
        """
        logging.info(message)
