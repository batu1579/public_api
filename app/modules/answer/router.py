#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-11-26 13:45:21
LastEditors: BATU1579
LastEditTime: 2021-11-26 15:44:27
Description: 获取答案的接口
'''
from fastapi import APIRouter

from .api.v1.router import router as v1


router = APIRouter(
    prefix='/chk_ans',
    tags=['答案API']
)

router.include_router(v1)
