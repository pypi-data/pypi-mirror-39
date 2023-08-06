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
# Backup status
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
BACKUP_FOLDER = os.path.join(DIR_PATH, 'log')


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


def get_logger(logname, always_use_stdout=True):
    log_format = '%(asctime)s ' + logname + ' %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_format, datefmt='%b %d %H:%M:%S')
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)

    if os.environ.get('PAPERTRAIL_HOST', None) is not None:
        logHandler = SysLogHandler(address=(os.environ.get('PAPERTRAIL_HOST'), int(os.environ.get('PAPERTRAIL_PORT'))))
        logHandler.addFilter(ContextFilter())
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)

    if always_use_stdout:
        stdoutLogHandler = logging.StreamHandler(sys.stdout)
        stdoutLogHandler.setFormatter(formatter)
        logger.addHandler(stdoutLogHandler)
    return logger


def set_backup_status(screen_name='unknown', status=None):
    if status is None:
        return
    backup_file = os.path.join(BACKUP_FOLDER, '{}.log'.format(screen_name))
    status_id = status.get('id_str', None)
    if status_id:
        with open(backup_file, 'w') as f:
            f.write(status_id)


def get_backup_status(screen_name='unknown'):
    backup_file = os.path.join(BACKUP_FOLDER, '{}.log'.format(screen_name))
    if not os.path.isfile(backup_file):
        return None
    with open(backup_file, 'r') as f:
        lines = f.read().splitlines()
        return int(lines[0]) if len(lines) > 0 else None
