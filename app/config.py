#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 19:31:13
LastEditor: BATU1579
LastTime: 2021-12-22 16:07:25
Description: 配置文件
'''
from os import getenv
from urllib.parse import quote_plus as qp


# ------------------------------------网站名称---------------------------------

DOMAIN = getenv('DOMAIN', 'batu1579.com')  # 网站域名

# ---------------------------------设置信任的域名-------------------------------

ORIGINS = [
        f"https://www.{DOMAIN}",
        f"http://www.{DOMAIN}",
        f"https://api.{DOMAIN}",
        f"http://api.{DOMAIN}",
        "https://localhost",
        "http://localhost"
]

# ---------------------------------设置数据库连接-------------------------------

MONGODB_URL = getenv('MONGODB_URL', None)

MAIN_DB_NAME = getenv('DB_NAME', 'server')

if (MONGODB_URL is None) or (MONGODB_URL == ""):
    MONGO_HOST = getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(getenv('MONGO_PORT', 27017))
    MONGO_USER = getenv("MONGO_USER", "admin")
    MONGO_PWD = getenv("MONGO_PASSWORD", "123456")
    MONGODB_URL = f'mongodb://{qp(MONGO_USER)}:{qp(MONGO_PWD)}@{qp(MONGO_HOST)}'

# ---------------------------------设置数据库集合名---------------------------------

AUTH_COLLECTION = 'auth'
