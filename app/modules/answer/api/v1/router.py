#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-11-26 13:51:10
LastEditor: BATU1579
LastTime: 2021-12-21 16:45:02
Description: 答案api v1路由
'''
from fastapi import APIRouter

from .course import router as course_router
from .question import router as question_router


router = APIRouter(prefix='/v1')

router.include_router(course_router)
router.include_router(question_router)
