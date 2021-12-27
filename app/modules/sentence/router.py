#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 18:06:39
LastEditor: BATU1579
LastTime: 2021-12-27 10:38:10
Description: 一言api路由
'''
from fastapi import APIRouter

from .api.v1.router import router as v1


router = APIRouter(tags=['一言API'])

router.include_router(v1)
