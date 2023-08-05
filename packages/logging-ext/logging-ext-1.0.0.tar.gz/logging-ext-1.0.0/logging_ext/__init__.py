#!/usr/bin/env python3

'''
logging ext module;
'''

from logging import *

DEBUG   = DEBUG
VERBOSE = INFO - 1
INFO    = INFO
WARN    = WARN
ERROR   = ERROR

def d(msg, *args, **kwargs):

    '''
    log a message at debug level;
    '''

    return log(DEBUG, msg, *args, **kwargs)

def v(msg, *args, **kwargs):

    '''
    log a message at verbose level;
    '''

    return log(VERBOSE, msg, *args, **kwargs)

def i(msg, *args, **kwargs):

    '''
    log a message at info level;
    '''

    return log(INFO, msg, *args, **kwargs)

def w(msg, *args, **kwargs):

    '''
    log a message at warn level;
    '''

    return log(WARN, msg, *args, **kwargs)

def e(msg, *args, **kwargs):

    '''
    log a message at error level;
    '''

    return log(ERROR, msg, *args, **kwargs)

def getLogger(name=None):

    '''
    override `logging.getLogger`; add additional methods to logger;
    '''

    import logging
    import types

    logger = logging.getLogger(name=name)

    if not hasattr(logger, 'd'):
        def d(self, msg, *args, **kwargs):
            return self.log(DEBUG, msg, *args, **kwargs)
        logger.d = types.MethodType(d, logger)

    if not hasattr(logger, 'v'):
        def v(self, msg, *args, **kwargs):
            return self.log(VERBOSE, msg, *args, **kwargs)
        logger.v = types.MethodType(v, logger)

    if not hasattr(logger, 'i'):
        def i(self, msg, *args, **kwargs):
            return self.log(INFO, msg, *args, **kwargs)
        logger.i = types.MethodType(i, logger)

    if not hasattr(logger, 'w'):
        def w(self, msg, *args, **kwargs):
            return self.log(WARN, msg, *args, **kwargs)
        logger.w = types.MethodType(w, logger)

    if not hasattr(logger, 'e'):
        def e(self, msg, *args, **kwargs):
            return self.log(ERROR, msg, *args, **kwargs)
        logger.e = types.MethodType(e, logger)

    return logger

