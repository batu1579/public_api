#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-11-26 13:56:46
LastEditor: BATU1579
LastTime: 2021-12-23 23:51:08
Description: 课程数据类
'''
from re import match
from pydantic import validator, BaseModel
from typing import Optional, List

from ..exception import ChapterNameInvalid
from ....models.base_model import (
    BaseMongoModel,
    InDBModel,
    InUpdateModel,
    CreateTime
)
from ..field import chapter_field


class Chapters(BaseModel):
    chapter: Optional[List[str]] = []  # 不能通过更新课程信息添加章节

    @validator('chapter', each_item=True)
    def check_chapter_name(cls, v):
        if match(chapter_field['regex'], v) is None:
            raise ChapterNameInvalid
        return v


class BaseCourse(BaseMongoModel, CreateTime):
    course_name: str
    description: str
    chapter: Optional[List[str]] = []


class CourseInCreate(BaseCourse):
    pass


class CourseInDB(InDBModel, BaseCourse):
    pass


class CourseInUpdate(InUpdateModel, CreateTime):
    course_name: Optional[str] = None
    description: Optional[str] = None


class CourseInResponse(BaseMongoModel):
    course: CourseInDB


class ManyCourseInResponse(BaseMongoModel):
    courses: List[CourseInDB]
