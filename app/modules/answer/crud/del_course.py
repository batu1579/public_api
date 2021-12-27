#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-20 21:36:27
LastEditor: BATU1579
LastTime: 2021-12-27 10:31:37
FilePath: \\app\\modules\\answer\\crud\\del_course.py
Description: 课程的删除操作
'''
from pymongo import ReturnDocument

from ....database.mongo import get_collection
from ..models.course import CourseInDB
from .question import (
    delete_question_by_course,
    delete_question_by_chapters
)
from ..exception import CourseNotFound
from ..config import COURSE_COLLECTION


async def delete_course(course_name: str) -> CourseInDB:
    '''删除指定课程'''
    await delete_question_by_course(course_name)
    collection = get_collection(COURSE_COLLECTION)
    result = await collection.find_one_and_delete(
        {'course_name': course_name},
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise CourseNotFound
    return CourseInDB.load_data(result)


async def delete_course_chapters(
        course_name: str,
        chapters: list) -> CourseInDB:
    '''删除课程章节'''
    await delete_question_by_chapters(course_name, chapters)
    collection = get_collection(COURSE_COLLECTION)
    result = await collection.find_one_and_update(
        {'course_name': course_name},
        {'$pullAll': {'chapter': chapters}},
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise CourseNotFound
    return CourseInDB.load_data(result)
