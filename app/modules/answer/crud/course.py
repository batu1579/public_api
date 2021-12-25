#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-11-26 15:59:19
LastEditor: BATU1579
LastTime: 2021-12-25 14:12:52
Description: 课程crud函数
'''
from pymongo import (
    DESCENDING,
    ReturnDocument
)
from pymongo.errors import DuplicateKeyError
from typing import List
from bson import ObjectId
from re import findall

from ....exception.error_code import ObjectIdInvalid
from ....database.mongo import get_collection
from ....models.object_id import OID
from ..models.course import (
    CourseInDB,
    CourseInUpdate,
    CourseInCreate
)
from ..exception import (
    CourseNotFound,
    CourseExists
)
from ..config import COURSE_COLLECTION


async def _get_course(quary: dict) -> CourseInDB:
    '''
    param {dict} quary 查询条件
    return {CourseInDB}
    description: 查询单个课程信息
    '''
    collection = get_collection(COURSE_COLLECTION)
    result = await collection.find_one(quary)

    if result is None:
        raise CourseNotFound

    return CourseInDB.load_data(result)


async def get_course_by_name(course_name: str) -> CourseInDB:
    '''通过课程名称获取课程信息'''
    return await _get_course({'course_name': course_name})


async def get_course_by_id(course_id: OID) -> CourseInDB:
    '''通过课程id获取课程信息'''
    if not ObjectId.is_valid(course_id):
        raise ObjectIdInvalid('course_id')
    return await _get_course({'_id': ObjectId(course_id)})


async def get_course_id(course_name: str) -> OID:
    '''通过课程名称获取课程id'''
    collection = get_collection(COURSE_COLLECTION)
    result = await collection.find_one({'course_name': course_name})

    if result is None:
        raise CourseNotFound

    return OID(result['_id'])


async def is_chapter_exists(course_name: str, chapter: str) -> bool:
    '''查询课程中是否存在该章节'''
    result = await get_course_by_name(course_name)
    return True if chapter in result.chapter else False


async def _get_courses(quary: dict, **kwargs):
    collection = get_collection(COURSE_COLLECTION)
    cursor = collection.find(
        quary, **kwargs
    ).sort('create_time', DESCENDING)
    data = []
    async for documents in cursor:
        data.append(CourseInDB.load_data(documents))
    return data


async def get_many_course(limit: int, skip: int) -> List[CourseInDB]:
    '''获取课程列表'''
    return await _get_courses({}, limit=limit, skip=skip)


async def search_courses(kw: str, limit: int, skip: int):
    kw = findall(r'[^\s\+]+', kw)
    return await _get_courses(
        {'$or': [{'course_name': {'$regex': course}} for course in kw]},
        limit=limit,
        skip=skip
    )


async def create_course(course: CourseInCreate) -> CourseInDB:
    '''新建一个新的课程'''
    collection = get_collection(COURSE_COLLECTION)
    try:
        result = await collection.insert_one(course.to_dict())
    except DuplicateKeyError:
        raise CourseExists
    return CourseInDB.load_data(
        {'_id': result.inserted_id, **course.to_dict()}
    )


async def update_course(
    course_name: str,
    course: CourseInUpdate
) -> CourseInDB:
    '''更新一个课程的信息'''
    collection = get_collection(COURSE_COLLECTION)
    result = await collection.find_one_and_update(
        {'course_name': course_name},
        {'$set': course.to_dict()},
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise CourseNotFound
    return CourseInDB.load_data(result)


async def update_course_chapters(
    course_name: str,
    chapters: list
) -> CourseInDB:
    '''添加课程章节'''
    collection = get_collection(COURSE_COLLECTION)
    result = await collection.find_one_and_update(
        {'course_name': course_name},
        {'$addToSet': {'chapter': {'$each': chapters}}},
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise CourseNotFound
    return CourseInDB.load_data(result)
