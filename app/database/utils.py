#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 18:25:47
LastEditors: BATU1579
LastEditTime: 2021-11-26 10:03:56
Description: 处理与数据库的连接
'''
from motor.motor_asyncio import AsyncIOMotorClient

from ..config import MONGODB_URL


class DBClient():
    client: AsyncIOMotorClient = None


DB = DBClient()


def connect_to_db():
    '''创建连接数据库的客户端'''
    DB.client = AsyncIOMotorClient(MONGODB_URL)


def close_connection():
    '''断开客户端与数据库的连接'''
    DB.client.close()
