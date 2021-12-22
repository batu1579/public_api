#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 20:08:43
LastEditor: BATU1579
LastTime: 2021-12-20 17:08:53
Description: 数据库操作
'''
from motor.motor_asyncio import AsyncIOMotorCollection

from .utils import DB
from ..config import MAIN_DB_NAME


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    '''获取数据库中的集合对象'''
    return DB.client[MAIN_DB_NAME][collection_name]
