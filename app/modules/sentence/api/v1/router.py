#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 18:09:22
LastEditors: BATU1579
LastEditTime: 2021-11-26 13:55:34
Description: 设置一言api v1路由
'''
from fastapi import APIRouter


router = APIRouter(
    prefix='/v1',
    tags=['v1']
)
