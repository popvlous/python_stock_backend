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
        'pyrarcdev',
        'dev2021api0322',
        '103.252.199.14',
        3306,
        'pcs'
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
        'id': 'bcjob',
        'func': 'jobs:bcjob',
        'trigger': 'interval',
        'seconds': 30
    }, {
        'id': 'bclitemjob',
        'func': 'jobs:bclitemjob',
        'trigger': 'interval',
        'seconds': 30
    }
    ]
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置時區


20
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
        'pyrarcdev',
        'dev2021api0322',
        '192.168.110.18',
        3306,
        'pcs'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
