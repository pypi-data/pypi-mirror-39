# coding: utf-8
# -*- coding: utf-8 -*-

__author__ = "Jalpesh Borad"
__copyright__ = "Copyright 2018"

__version__ = "0.0.1"
__maintainer__ = "Jalpesh Borad"
__email__ = "jalpeshborad@gmail.com"
__status__ = "Development"

import logging
import os


def init_logger(name, base_dir=None):
    """
    Logger with Stram and File handler
    :param name: Name of logger
    :param base_dir: Full path of directory where log files is to be stored,
                    If None, it will create logs folder in HOME directory
    :return: Logger object
    """
    if not base_dir:
        base_dir = os.path.join(os.getenv("HOME"), "logs")

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not len(logger.handlers):
        formatter = logging.Formatter(
            "%(asctime)s [%(name)s] [%(levelname)s] [PID: %(process)d]"
            " [%(module)s ==> %(funcName)s] [Line no: %(lineno)d] %(message)s"
            , datefmt="%d/%m/%Y %I:%M:%S %p")
        stream_logs = logging.StreamHandler()
        if not os.path.exists(os.path.join(base_dir, name)):
            os.mkdir(os.path.join(base_dir, name))
        log_file = logging.FileHandler(
            os.path.join(base_dir, name, "{}.log".format(name)))
        stream_logs.setFormatter(formatter)
        log_file.setFormatter(formatter)
        logger.addHandler(stream_logs)
        logger.addHandler(log_file)
    return logger
