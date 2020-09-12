# -*- coding: utf-8 -*-
# License: GPL-2.0+ <http://spdx.org/licenses/GPL-2.0+>

from __future__ import absolute_import
import sys
import os
import logging
import logging.handlers
import traceback
import time
import getpass

logger = logging.getLogger('fedora-release-autotest')
logger.addHandler(logging.NullHandler())  

# log formatting
_fmt_full = '[%(name)s:%(filename)s:%(lineno)d] '\
            '%(asctime)s %(levelname)-7s %(message)s'
_fmt_simple = '[%(name)s] %(asctime)s %(levelname)-7s %(message)s'
_datefmt_full = '%Y-%m-%d %H:%M:%S'
_datefmt_simple = '%H:%M:%S'
_formatter_full = logging.Formatter(fmt=_fmt_full, datefmt=_datefmt_full)
_formatter_simple = logging.Formatter(fmt=_fmt_simple, datefmt=_datefmt_simple)
# set logging time to UTC/GMT
_formatter_full.converter = time.gmtime
_formatter_simple.converter = time.gmtime


def logger_init(log_level=None, filelog_path=None):

    rootlogger = logging.getLogger()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(_formatter_simple)

    if filelog_path is None:
        filelog_path = os.path.join('/tmp', 'fedora-autotest-%s.log' % time.strftime("%Y%m%d%H"))

    file_handler = logging.FileHandler(filelog_path, encoding='UTF-8')
    file_handler.setFormatter(_formatter_full)

    # try access
    try:
        f = open(filelog_path, 'a')
        f.write('#'*120 + '\n')
        f.close()
    except IOError as e:
        log.error("Log file can't be opened for writing: %s\n  %s", filelog_path, e)
        raise

    if log_level:
        stream_handler.setlevel(log_level)
        file_handler.setlevel(log_level)

    rootlogger.addHandler(stream_handler)
    rootlogger.addHandler(file_handler)

    logger.debug('File logging enabled with level %s into: %s',
              logging.getLevelName(file_handler.level), filelog_path)

