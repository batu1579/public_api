#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 17:58:20
LastEditors: BATU1579
LastEditTime: 2021-11-30 09:09:40
Description: 设置公共API路由
'''
from fastapi import APIRouter

from .sentence.router import router as r_sentence
from .answer.router import router as r_answer


public_api_router = APIRouter(
    prefix='/public',
    tags=['公共api']
)

public_api_router.include_router(r_sentence)
public_api_router.include_router(r_answer)
