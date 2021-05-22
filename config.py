'''Параметры конфигурации приложения'''


class Config(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///weather.db'
    SECRET_KEY = 'confidential!'
    DEBUG = True
    LOGFILE = 'logs.log'
    TESTING = False
