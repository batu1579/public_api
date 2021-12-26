#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-26 23:23:21
LastEditor: BATU1579
LastTime: 2021-12-26 23:36:39
FilePath: \\app\\modules\\sentence\\models\\sentence.py
Description: 句子数据类
'''
from typing import Optional, List

from ....models.base_model import (
    BaseMongoModel,
    InUpdateModel,
    InDBModel,
    CreateTime
)
from ....models.object_id import OID


class BaseSentence(BaseMongoModel, CreateTime):
    sentence: str
    citations: str
    tags: List[OID]


class SentenceInCreate(BaseSentence):
    pass


class SentenceInDB(InDBModel, BaseSentence):
    pass


class SentenceInUpdate(InUpdateModel):
    sentence: Optional[str] = None
    citations: Optional[str] = None
    tags: Optional[List[OID]] = None


class SentenceInResponse(BaseMongoModel):
    sentence: SentenceInDB


class ManySentenceInResponse(BaseMongoModel):
    sentences: List[SentenceInDB]
