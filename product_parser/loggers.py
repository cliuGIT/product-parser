# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 2012

@author: cliu
"""

import logging
import logging.handlers


def create_simple_logger(name='Logger', level='DEBUG', echo=True, path=''):
    """
    Create a simple logger:
    
    name        logger name.
    level       a string, one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
    echo        whether to print log in shell.
    path        full path name of log file.
    
    return a logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        if level == 'DEBUG':
            logger.setLevel(logging.DEBUG)
        elif level == 'INFO':
            logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            logger.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            logger.setLevel(logging.CRITICAL)
        else:
            return None

        if path:
            fh = logging.handlers.TimedRotatingFileHandler(path,
                when='D', interval=1, backupCount=30, encoding='utf8')
            fh.setLevel(logging.DEBUG)
            ffmt = logging.Formatter("%(asctime)s\t%(name)s\t%(levelname)s\t%(thread)d\t%(filename)s\t%(funcName)s\t%(message)s")
            fh.setFormatter(ffmt)
            logger.addHandler(fh)

        if echo:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            cfmt = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
            ch.setFormatter(cfmt)
            logger.addHandler(ch)

    return logger

