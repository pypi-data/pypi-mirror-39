# -*- coding: utf-8 -*-

import logging
import os
import socket
import sys
from logging.handlers import SysLogHandler

# ggtrans limit 1500 characters
MAX_CONTENT_GG_LENGTH = 1500
# discord limit 2000 characters
MAX_CONTENT_DISCORD_LENGTH = 2000
# MAX_RE_TRY
MAX_RE_TRY = os.environ.get('MAX_RE_TRY', 3)
# DELAY
DELAY = os.environ.get('DELAY', 1)  # seconds


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


def fix_max_length(text_content, max_length=MAX_CONTENT_GG_LENGTH):
    """Convert long text to valid array text

    Arguments:
        text_content

    Keyword Arguments:
        max_length {[int]} -- (default: {MAX_CONTENT_GG_LENGTH})

    Returns:
        array
    """
    text_array = []
    if len(text_content) <= max_length:
        return [text_content]
    text_cache = text_content
    while len(text_cache) > max_length:
        text_cut = text_cache[:max_length]
        try:
            last_break_line = text_cut.rindex('\n')
        except ValueError:
            last_break_line = len(text_cut)
        text_array.append(text_cut[:last_break_line])
        text_cache = text_cache[last_break_line:]
    text_array.append(text_cache)
    return text_array


def get_logger(logname):
    log_format = '%(asctime)s ' + logname + ' %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_format, datefmt='%b %d %H:%M:%S')
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)

    if os.environ.get('PAPERTRAIL_HOST', None) is not None:
        logHandler = SysLogHandler(address=(os.environ.get('PAPERTRAIL_HOST'), int(os.environ.get('PAPERTRAIL_PORT'))))
        logHandler.addFilter(ContextFilter())
    else:
        logHandler = logging.StreamHandler(sys.stdout)

    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    return logger
