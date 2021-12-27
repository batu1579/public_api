#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-26 23:23:21
LastEditor: BATU1579
LastTime: 2021-12-27 12:56:00
FilePath: \\app\\modules\\sentence\\models\\sentence.py
Description: 句子数据类
'''
from re import match
from typing import Optional, List
from pydantic import BaseModel, validator

from ....models.base_model import (
    BaseMongoModel,
    InUpdateModel,
    InDBModel,
    CreateTime
)
from ..exception import TagInvalid


class Tags(BaseModel):
    tags: Optional[List[str]] = []

    @validator('tags', each_item=True)
    def check_tags(cls, v):
        if match(r'^[\u4e00-\u9fa5a-zA-Z0-9]+$', v) is None:
            raise TagInvalid
        return v


class BaseSentence(BaseMongoModel, CreateTime):
    sentence: str
    attribution: str
    tags: List[str]


class SentenceInCreate(BaseSentence):
    pass


class SentenceInDB(InDBModel, BaseSentence):
    pass


class SentenceInUpdate(InUpdateModel):
    sentence: Optional[str] = None
    attribution: Optional[str] = None
    tags: Optional[List[str]] = None


class SentenceInResponse(BaseMongoModel):
    sentence: SentenceInDB


class ManySentenceInResponse(BaseMongoModel):
    sentences: List[SentenceInDB]
