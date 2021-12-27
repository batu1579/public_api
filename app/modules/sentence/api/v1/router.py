#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 18:09:22
LastEditor: BATU1579
LastTime: 2021-12-27 13:13:22
Description: 设置一言api v1路由
'''
from fastapi import APIRouter

from .sentence import router as sentence_router


router = APIRouter(prefix='/v1')

router.include_router(sentence_router)
