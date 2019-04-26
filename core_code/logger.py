# -*- coding: utf-8 -*-
import logging
import os


LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'logs'


class Logging():
    def __init__(self, file_name):
        """
        constructor
        """
        path = os.path.dirname(os.getcwd())+'/'+LOG_DIR
        if not os.path.isdir(path):
            os.makedirs(path)

        # Create a custom logger
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(LOG_LEVEL)

        # Create handler
        f_handler = logging.FileHandler(path+'/'+file_name+'.log')
        f_handler.setLevel(LOG_LEVEL)

        # Create the formatter and add it to handler
        formatter = logging.Formatter(LOG_FORMAT)
        f_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(f_handler)
