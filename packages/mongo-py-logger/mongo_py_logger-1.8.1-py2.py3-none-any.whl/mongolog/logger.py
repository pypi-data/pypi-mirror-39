import json
import logging
import ssl

import time

import datetime
from bson import json_util

from handlers import MongoHandler, MongoFormatter


class MongoLogger(logging.Logger):
    def __init__(self, mongodb_connection_string, cert_path=None, ca_cert_path=None, name=None,
                 collection_name='logs_collection', **kwargs):
        """
        :param mongodb_connection_string: connection string to mongoDB with format:
        mongodb://[username]:[password]@[host:port,host:port]/[db name]?ssl=true&replicaSet=mongo7581
        :param cert_path: path to cert file (*.pem)
        :param job_id: id of Job instance (filename with logs will be job_id number)
        :param name: Name of the logger (logging channel), default value: 'self.__class__.__name__'
        :param dir_pth: path to save .log file, default value: 'logs'
        For adding extra field to special log: logger.debug("my log", extra={'field': 'my value'})
        For traceback: self.logger.error("Some error", exc_info=True)
        """
        self.kwarg = kwargs
        self.__collection_name = collection_name
        self.__cert_path = cert_path
        self.__ca_cert_path = ca_cert_path
        self.__db_name = mongodb_connection_string.split('/')[-1].split('?')[0]
        name = name or self.__class__.__name__
        super(MongoLogger, self).__init__(name)
        self.__config_handlers(mongodb_connection_string)

    def __config_handlers(self, mongodb_connection_string):
        json_stringify_formatter, text_formatter = self.__config_formatters()
        console_info_handler = logging.StreamHandler()
        console_info_handler.setFormatter(text_formatter)
        if self.__cert_path:
            mongodb_handler = MongoHandler(
                host=mongodb_connection_string,
                database_name=self.__db_name,
                collection=self.__collection_name,
                formatter=MongoFormatter(json_stringify_formatter),
                authentication_db=None,
                ssl=True,
                ssl_certfile=self.__cert_path,
                ssl_cert_reqs=ssl.CERT_REQUIRED,
                ssl_ca_certs=self.__ca_cert_path)
        else:
            mongodb_handler = MongoHandler(
                host=mongodb_connection_string,
                database_name=self.__db_name,
                collection=self.__collection_name,
                formatter=MongoFormatter(json_stringify_formatter),
                authentication_db=None,
                ssl=False)
        self.addHandler(console_info_handler)
        self.addHandler(mongodb_handler)

    def __config_formatters(self):
        # set a format which is simpler for console and file use
        log_formatter = logging.Formatter(
            "[%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(processName)s - %(threadName)s] %(message)s"
        )
        log_formatter.converter = time.gmtime
        # set a json format
        json_format = {
            'debug': {
                'levelname': '%(levelname)s',
                'name': '%(name)s',
                'module': '%(module)s',
                'process': '%(process)d',
                'processName': '%(processName)s',
                'thread': '%(thread)d',
                'threadName': '%(threadName)s',
                'pathname': '%(pathname)s',
                'filename': '%(filename)s',
                'funcName': '%(funcName)s',
                'lineno': '%(lineno)d',
            },
            'levelname': '%(levelname)s',
            'message': '%(message)s',
            'asctime': '%(asctime)s'
        }
        for key, val in self.kwarg.items():
            json_format[key] = val
        json_stringify_formatter = logging.Formatter(json.dumps(json_format))
        json_stringify_formatter.converter = time.gmtime
        return json_stringify_formatter, log_formatter

    def pull_logs(self, query):
        """
        :return: json data
        """
        mongo_handler = [handler for handler in self.handlers if isinstance(handler, MongoHandler)]
        logs = list(mongo_handler[0].connection[self.__db_name][self.__collection_name].find(query))
        logs = json.dumps(logs, default=json_util.default)
        return json.loads(logs)
