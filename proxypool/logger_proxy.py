import logging.config
import os
import logging.handlers
import yaml
import logging


"""
class mylogger(object):
    log_path = os.path.join(os.curdir,'logs')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_name = datetime.datetime.now().strftime('%y-%m-%d') + '.log'
    logger_conf_path =os.path.join(os.curdir,'logging.conf')
    @staticmethod
    def init_log_conf():
        logging.config.fileConfig(mylogger.logger_conf_path)
    @staticmethod
    def get_logger(name=''):
        mylogger.init_log_conf()
        return logging.getLogger(name)
"""
# log_name = datetime.datetime.now().strftime('%y-%m-%d') + '.log'


class MyLogger(object):
    log_path = os.path.join(os.curdir, 'logs')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    print(os.curdir)

    logger_conf_path = os.path.join(os.curdir, 'logging.yaml')
    with open(logger_conf_path, 'r') as log_conf:
        dict_yaml = yaml.load(log_conf)

    @staticmethod
    def init_log():
        logging.config.dictConfig(MyLogger.dict_yaml)

    @staticmethod
    def get_logger(name=''):
        MyLogger.init_log()
        return logging.getLogger(name)
