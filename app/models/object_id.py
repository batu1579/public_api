#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 20:30:41
LastEditors: BATU1579
LastEditTime: 2021-10-07 20:39:10
Description: 格式化ObjectID
'''
from bson import ObjectId


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not isinstance(value, ObjectId):
            raise TypeError('ObjectId required')
        return ObjectId(str(value))
