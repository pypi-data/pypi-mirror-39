# -*- coding: utf-8 -*-

import sys
import os
import os.path
from io import StringIO

import collections

import json

from datetime import datetime
from datetime import timedelta

import argparse
import configparser
import logging
from logging.handlers import RotatingFileHandler

logging.NOTICE = 25
logging.NOTICE_LEVEL_NAME = "NOTICE"

logging.addLevelName(logging.NOTICE, logging.NOTICE_LEVEL_NAME)
def notice(self, message, *args, **kws):
    self._log(logging.NOTICE, message, args, **kws) 
logging.Logger.notice = notice

class Config:

    def __init__(self, **kwargs):
        self.argparser = argparse.ArgumentParser(kwargs)
        self.argparser.add_argument('-c', '--config'
                                    , metavar='PATH'
                                    , default='config.ini'
                                    , help='設定ファイルへのパス')
        self.argparser.add_argument('--verbose'
                                    , action="store_true"
                                    , default=False
                                    , help='詳細なデータを出力')
        self.argparser.add_argument('--debug'
                                    , action="store_true"
                                    , default=False
                                    , help='デバグモードで実行')
        self.argparser.add_argument('--debug_file'
                                    , metavar='FILE'
                                    , help='デバグモードで実行しファイル出力')

    def parse(self, config = None):
        self.args = self.argparser.parse_args()
        self.parser = configparser.ConfigParser()
        self.ini = collections.defaultdict(dict)
        self.err = []
        self.config_path = config if config else self.args.config
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    self.parser.read_file(f)
                    if self.parser.has_option("CONFIG", "base"):
                        with open(self.parser.get("CONFIG", "base"), "r") as f2:
                            self.parser.read_file(f2)
                    #read again to override
                    self.parser.read_file(f)
            except Exception as e:
                self.err.append('設定ファイル[{}]の読み込みに失敗しました。エラー：{}'.format(self.config_path, e))
        else:
            self.err.append('設定ファイル[{}]が見つかりません。'.format(self.config_path))

    def load_attr(self, attr, section, option, required=True, default=None):
        value = self.parser.get(section, option) if required or self.parser.has_option(section, option) else default
        self.ini[section][attr] = value
        setattr(self, attr, value)

    def load_attr_boolean(self, attr, section, option, required=True, default=False):
        value = self.parser.getboolean(section, option) if required or self.parser.has_option(section, option) else default
        self.ini[section][attr] = value
        setattr(self, attr, value)

    def load_attr_int(self, attr, section, option, required=True, default=False):
        value = self.parser.getint(section, option) if required or self.parser.has_option(section, option) else default
        self.ini[section][attr] = value
        setattr(self, attr, value)

    def load_attr_float(self, attr, section, option, required=True, default=False):
        value = self.parser.getfloat(section, option) if required or self.parser.has_option(section, option) else default
        self.ini[section][attr] = value
        setattr(self, attr, value)

    def load_attr_dict(self, attr, section, option, required=True, raise_error=True, default={}):
        self.load_attr_json(attr, section, option, required, raise_error, default)
        
    def load_attr_list(self, attr, section, option, required=True, raise_error=True, default=[]):
        self.load_attr_json(attr, section, option, required, raise_error, default)
        
    def load_attr_json(self, attr, section, option, required, raise_error, default):
        value_string = self.parser.get(section, option) if required or self.parser.has_option(section, option) else None
        if value_string:
            try:
                value_json = json.loads(value_string)
                value_error = None
            except Exception as e:
                value_json = default
                value_error = e
                self.err.append('オプション[{}][{}]の読み込みに失敗しました。エラー：{}'.format(section, option, e))
                if required or raise_error:
                    raise e
        else:
            value_string = json.dump(default)
        self.ini[section][attr] = value_string
        if value_error:
            self.ini[section][attr+"_error"] = value_error
        setattr(self, attr, value_json)
        setattr(self, attr+"_string", value_string)
        setattr(self, attr+"_error", value_error)

    def load_logging(self
                     , log_level=logging.DEBUG
                     , log_file=""
                     , log_max_bytes = 1024*1024*16
                     , log_backup_count = 99
                     , log_encoding = 'UTF-8'):
        self.verbose = self.args.verbose
        self.log_level = log_level
        self.log_level_name = logging.getLevelName(log_level)
        self.log_file = log_file
        self.log_max_bytes = log_max_bytes
        self.log_backup_count = log_backup_count
        self.log_encoding = log_encoding

        if self.parser.has_section('Logging'):
            section = self.parser['Logging']
            self.verbose = section.get('verbose', self.verbose)
            self.log_level_name = section.get('level', 'INFO')
            self.log_level = getattr(logging, self.log_level_name.upper(), self.log_level)
            self.log_file = section.get('log file', self.log_file)
            self.err_file = section.get('err file', '')
            self.log_encoding = section.get('encoding', self.log_encoding)
            bytes_str = section.get("max bytes", '').replace('(','').replace(')','').replace('=','')
            self.log_max_bytes = eval(bytes_str) if bytes_str else self.log_max_bytes
            self.log_backup_count = int(section.get('backup count', self.log_backup_count))

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)
        self.formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        if self.args.debug:
            handler = logging.StreamHandler()
            handler.setFormatter(self.formatter)
            handler.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)
        if self.args.debug_file:
            try:
                handler = FileHandler(self.args.debug_file, encoding = self.log_encoding)
                handler.setFormatter(self.formatter)
                handler.setLevel(logging.DEBUG)
                self.logger.addHandler(handler)
                self.logger.setLevel(logging.DEBUG)
            except Exception as e:
                self.err.append('DEBUG FILEログ設定に失敗しました。ファイル：[{}] エラー：[{}]'.format(self.args.debug_file, e))
        if self.log_file:
            try:
                handler = RotatingFileHandler(self.log_file, maxBytes = self.log_max_bytes, backupCount = self.log_backup_count, encoding = self.log_encoding)
                handler.setFormatter(self.formatter)
                self.logger.addHandler(handler)
            except Exception as e:
                self.err.append('ログ設定に失敗しました。ファイル：[{}] エラー：[{}]'.format(self.log_file, e))
        if hasattr(self, 'err_file') and self.err_file and self.err_file != self.log_file:
            try:
                handler = RotatingFileHandler(self.err_file, maxBytes = self.log_max_bytes, backupCount = self.log_backup_count, encoding = self.log_encoding)
                handler.setFormatter(self.formatter)
                handler.setLevel(logging.ERROR)
                self.logger.addHandler(handler)
            except Exception as e:
                self.err.append('エラーログ設定に失敗しました。ファイル：[{}] エラー：[{}]'.format(self.err_file, e))
        if len(self.logger.handlers) == 0:
            handler = logging.StreamHandler()
            handler.setFormatter(self.formatter)
            handler.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)
            self.logger.warn("ログの出力先が標準出力に設定されました。")
        
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("DEBUGモードが有効になりました。")
        elif self.logger.isEnabledFor(logging.INFO):
            self.logger.info("ログ設定が有効になりました。INFOログが出力されます。")
        elif self.logger.isEnabledFor(logging.NOTICE):
            self.logger.notice("ログ設定が有効になりました。NOTICEログが出力されます。")
        elif self.logger.isEnabledFor(logging.WARN):
            self.logger.warn("ログ設定が有効になりました。WARNINGログが出力されます。")

    def __repr__(self):
        with StringIO() as out:
            print('Configuration:', file=out)
            print('- Command Line Input: {}'.format(self.args), file=out)
            print('- Logging Configuration: Level={}->{} File={} MaxBytes={} Backup={}'.format(self.log_level_name, self.log_level, self.log_file, self.log_max_bytes, self.log_backup_count), file=out)
            for section, values in self.ini.items():
                print('- {}: {}'.format(section, values), file=out)
            print('- Configuration Error: {}'.format(self.err), file=out)
            return out.getvalue()

