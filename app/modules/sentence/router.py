#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 18:06:39
LastEditors: BATU1579
LastEditTime: 2021-10-07 18:14:43
Description: 一言api路由
'''
from fastapi import APIRouter

from .api.v1.router import router as v1


router = APIRouter(
    prefix='/sentence',
    tags=['一言API']
)

router.include_router(v1)
