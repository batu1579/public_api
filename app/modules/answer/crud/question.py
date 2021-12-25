#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-11-30 08:52:07
LastEditor: BATU1579
LastTime: 2021-12-25 14:13:07
Description: 问题CRUD函数
'''
from pymongo import DESCENDING, ReturnDocument
from pymongo.errors import DuplicateKeyError
from typing import List
from bson import ObjectId
from re import findall

from ....exception.error_code import ObjectIdInvalid
from ....database.mongo import get_collection
from ....models.object_id import OID
from ..crud.course import is_chapter_exists, get_course_id
from ..models.question import (
    QuestionInDB,
    QuestionInCreate,
    QuestionInUpdate
)
from ..exception import (
    AnsExists,
    AnsNotFound,
    ChapterNotFound
)
from ..config import ANS_COLLECTION


async def _get_ans(quary: dict) -> dict:
    '''获取单个答案'''
    collection = get_collection(ANS_COLLECTION)
    result = await collection.find_one(
        filter=quary
    )

    if result is None:
        raise AnsNotFound

    return QuestionInDB.load_data(result)


async def get_ans_by_question(question: str) -> dict:
    '''通过问题获取答案(正则匹配的第一个)'''
    return await _get_ans({'question': {'$regex': question}})


async def get_ans_by_question_id(question_id: OID) -> dict:
    '''通过问题id获取答案'''
    if not ObjectId.is_valid(question_id):
        raise ObjectIdInvalid('question_id')
    return await _get_ans({'_id': ObjectId(question_id)})


async def _get_many_ans(quary: dict, **kwargs) -> List[dict]:
    collection = get_collection(ANS_COLLECTION)
    cursor = collection.find(
        filter=quary,
        **kwargs
    ).sort('create_time', DESCENDING)

    data = []
    async for documents in cursor:
        documents = QuestionInDB.load_data(documents)
        data.append(documents)
    return data


async def get_ans_by_chapter(
        course_name: str,
        chapter: str) -> List[dict]:
    '''获取章节的全部答案'''
    if not await is_chapter_exists(course_name, chapter):
        raise ChapterNotFound

    course_id = await get_course_id(course_name)

    return await _get_many_ans({
        'course': ObjectId(course_id),
        'chapter': chapter
    })


async def get_ans_by_regex(kw: str, limit: int, skip: int) -> List[dict]:
    '''通过不完整的问题获取问题的答案（正则表达式）'''
    kw = findall(r'[^\+\s]+', kw)
    return await _get_many_ans(
        {'$or': [{'question': {'$regex': ans}} for ans in kw]},
        limit=limit,
        skip=skip
    )


async def create_question(
        course_name: str,
        question: QuestionInCreate) -> QuestionInDB:
    '''添加一个题目'''
    if not await is_chapter_exists(course_name, question.chapter):
        raise ChapterNotFound
    collection = get_collection(ANS_COLLECTION)
    try:
        result = await collection.insert_one(question.to_dict())
    except DuplicateKeyError:
        raise AnsExists
    return QuestionInDB.load_data(
        {'_id': result.inserted_id, **question.to_dict()}
    )


async def update_question(
        question_id: OID,
        new_question: QuestionInUpdate) -> QuestionInDB:
    '''更新问题'''
    if not ObjectId.is_valid(question_id):
        raise ObjectIdInvalid('question_id')

    collection = get_collection(ANS_COLLECTION)
    result = await collection.find_one_and_update(
        {'_id': ObjectId(question_id)},
        {'$set': new_question.to_dict()},
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise AnsNotFound
    return QuestionInDB.load_data(result)


async def delete_question(question: str):
    '''删除指定问题'''
    collection = get_collection(ANS_COLLECTION)
    result = await collection.find_one_and_delete(
        {'question': question}
    )
    if result is None:
        raise AnsNotFound
    return QuestionInDB.load_data(result)


async def delete_question_by_id(question_id: OID) -> QuestionInDB:
    '''删除指定id的问题'''
    if not ObjectId.is_valid(question_id):
        raise ObjectIdInvalid('question_id')
    collection = get_collection(ANS_COLLECTION)
    result = await collection.find_one_and_delete(
        {'_id': ObjectId(question_id)}
    )
    if result is None:
        raise AnsNotFound
    return QuestionInDB.load_data(result)


async def _del_many_question(quary: dict):
    collection = get_collection(ANS_COLLECTION)
    await collection.delete_many(quary)


async def delete_question_by_chapters(
        course_name: str,
        chapters: list):
    '''删除多个章节的问题'''
    course_id = await get_course_id(course_name)
    await _del_many_question({
        '$or': [{'course': ObjectId(course_id), 'chapter': i} for i in chapters]
    })


async def delete_question_by_course(course_name: str):
    '''删除整个课程的题目'''
    course_id = await get_course_id(course_name)
    await _del_many_question({'course': ObjectId(course_id)})
