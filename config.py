# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import pymysql

pymysql.install_as_MySQLdb()


class Config(object):
    # This will create a file in <app> FOLDER
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?autocommit=true'.format(
        'mysql',
        'civetpublic',
        'Foxconn99',
        '104.155.228.163',
        3306,
        'openfire'
        # 'mysql',
        # 'root',
        # 'root',
        # '127.0.0.1',
        # 3306,
        # 'pcs'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    JOBS = [{
        'id': 'sendActionRecordJob',
        'func': 'jobs:sendActionRecordJob',
        'trigger': 'interval',
        'seconds': 10
    }]
    #
    # JOBS = [{
    #     'id': 'sendActionRecordJob',
    #     'func': 'jobs:sendActionRecordJob',
    #     'trigger': 'cron',
    #     'day_of_week': '*',
    #     'hour': 16,
    #     'minute': 17,
    #     'second': 10,
    # }]

    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置時區

    DOMAIN_URL = 'https://member-api.tpp.org.tw/'
    DATA_TOKEN = 'ENXsCAbfyXYqincPulKe'

SCHEDULER_API_ENABLED = True  # 新增API


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?autocommit=true'.format(
        'mysql',
        'civetpublic',
        'Foxconn99',
        '10.47.144.3',
        3306,
        'civet_public_srv'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    JOBS = [{
        'id': 'sendActionRecordJob',
        'func': 'jobs:sendActionRecordJob',
        'trigger': 'interval',
        'seconds': 10
    }]

    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置時區

    DOMAIN_URL = 'https://member-api.tpp.org.tw/'
    DATA_TOKEN = 'ENXsCAbfyXYqincPulKe'


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
