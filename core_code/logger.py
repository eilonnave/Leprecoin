# -*- coding: utf-8 -*-
import logging
import os


LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'logs'


class Logger():
    def __init__(self, file_name):
        """
        constructor
        """
        path = os.path.dirname(os.getcwd())+'/'+LOG_DIR
        if not os.path.isdir(path):
            os.makedirs(path)
        logging.basicConfig(format=LOG_FORMAT,
                            filename=path+'/'+file_name,
                            level=LOG_LEVEL)

    @staticmethod
    def info(message):
        """
        the function adds info message to the
        logging
        :param message: the message to logging
        """
        logging.info(message)
