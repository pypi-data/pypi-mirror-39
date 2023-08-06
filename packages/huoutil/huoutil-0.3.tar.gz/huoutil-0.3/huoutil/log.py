#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import json


class Logger(object):
    def __init__(self,
            log_path,
            level=logging.INFO,
            stdout=False,
            when="D",
            backup=7,
            format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"):
        """
        init_log - initialize log module

        Args:
          log_path      - Log file path prefix.
                          Log data will go to two files: log_path.log and log_path.log.wf
                          Any non-exist parent directories will be created automatically
          level         - msg above the level will be displayed
                          DEBUG < INFO < WARNING < ERROR < CRITICAL
                          the default value is logging.INFO
          when          - how to split the log file by time interval
                          'S' : Seconds
                          'M' : Minutes
                          'H' : Hours
                          'D' : Days
                          'W' : Week day
                          default value: 'D'
          format        - format of the log
                          default format:
                          %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                          INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
          backup        - how many backup file to keep
                          default value: 7

        Raises:
            OSError: fail to create log directories
            IOError: fail to open log file

        Example:
        init_log("./log/my_program")  # 日志保存到./log/my_program.log和./log/my_program.log.wf，按天切割，保留7天
        logging.info("Hello World!!!")

        """
        self._logger = None

        formatter = logging.Formatter(format, datefmt)
        logger = logging.getLogger()
        logger.setLevel(level)

        dir = os.path.dirname(log_path)
        if not dir:
            dir = './'
        if not os.path.isdir(dir):
            os.makedirs(dir)

        if stdout:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(level)
            stdout_handler.setFormatter(formatter)
            logger.addHandler(stdout_handler)

        handler = logging.handlers.TimedRotatingFileHandler(
            log_path + ".log", when=when, backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        # https://www.jianshu.com/p/25f70905ae9d
        handler.suffix = '%Y-%m-%d'
        logger.addHandler(handler)

        err_handler = logging.handlers.TimedRotatingFileHandler(
            log_path + ".log.wf", when=when, backupCount=backup)
        err_handler.setLevel(logging.WARNING)
        err_handler.setFormatter(formatter)
        handler.suffix = '%Y-%m-%d'
        logger.addHandler(err_handler)
        self._logger = logger
        return logger

    def convert_msg(self, msg):
        if isinstance(msg, dict):
            _msg = json.dumps(msg, ensure_ascii=False)
        else:
            _msg = msg
        return _msg

    def debug(self, msg, *args, **kwargs):
        _msg = self.convert_msg(msg)
        self._logger.debug(_msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        _msg = self.convert_msg(msg)
        self._logger.info(_msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        _msg = self.convert_msg(msg)
        self._logger.warning(_msg, *args, **kwargs)

    warn = warning

    def error(self, msg, *args, **kwargs):
        _msg = self.convert_msg(msg)
        self._logger.error(_msg, *args, **kwargs)


    def exception(self, msg, *args, **kwargs):
        _msg = self.convert_msg(msg)
        self._logger.exception(_msg, *args, **kwargs)


    def critical(self, msg, *args, **kwargs):
        _msg = self.convert_msg(msg)
        self._logger.critical(_msg, *args, **kwargs)

    def ls_msg(self, es_index, es_type, msg):
        if isinstance(msg, dict):
            _msg = json.dumps(msg, ensure_ascii=False)
        else:
            _msg = msg
        _msg = u'logstash###{}###{}###{}'.format(es_index, es_type, _msg)
        return _msg

    def ls_debug(self, es_index, es_type, msg):
        """
        logstash debug
        """
        _msg = self.ls_msg(es_index, es_type, msg)
        self._logger.debug(_msg)

    def ls_info(self, es_index, es_type, msg):
        _msg = self.ls_msg(es_index, es_type, msg)
        self._logger.info(_msg)

    def ls_warning(self, es_index, es_type, msg):
        _msg = self.ls_msg(es_index, es_type, msg)
        self._logger.warning(_msg)

    ls_warn = ls_warning

    def ls_error(self, es_index, es_type, msg):
        _msg = self.ls_msg(es_index, es_type, msg)
        self._logger.error(_msg)

    def ls_critical(self, es_index, es_type, msg):
        _msg = self.ls_msg(es_index, es_type, msg)
        self._logger.critical(_msg)
