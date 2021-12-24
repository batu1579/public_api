#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-11-26 14:34:43
LastEditor: BATU1579
LastTime: 2021-12-23 23:52:01
Description: 题目数据类
'''
from typing import Optional, List
from pydantic import validator, BaseModel
from re import match

from ....models.base_model import (
    InDBModel,
    BaseMongoModel,
    CreateTime,
    InUpdateModel
)
from ....models.object_id import OID
from ..exception import AnswerInvalid


class Answer(BaseModel):
    answer: List[str]

    @validator('answer', each_item=True)
    def check_answer(cls, v):
        if match(r'^[\$]$', v) is None:
            raise AnswerInvalid
        return v


class BaseQuestion(BaseMongoModel, CreateTime):
    question: str
    course: OID
    chapter: str
    answer: List[str]


class QuestionInCreate(BaseQuestion):
    pass


class QuestionInDB(InDBModel, BaseQuestion):
    pass


class QuestionInUpdate(InUpdateModel):
    question: Optional[str] = None
    answer: Optional[List[str]] = None
    course: Optional[OID] = None
    chapter: Optional[str] = None


class QuestionInResponse(BaseMongoModel):
    question: dict


class ManyQuestionsInResponse(BaseMongoModel):
    questions: List[dict]


class DetailQuestionInResponse(BaseMongoModel):
    question: QuestionInDB
