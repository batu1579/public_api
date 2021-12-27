#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-26 23:37:13
LastEditor: BATU1579
LastTime: 2021-12-27 10:56:51
FilePath: \\app\\modules\\sentence\\curd\\sentence.py
Description: 句子crud函数
'''
from re import findall
from bson import ObjectId
from typing import List, Optional
from pymongo.errors import DuplicateKeyError
from pymongo import DESCENDING, ReturnDocument

from ....models.object_id import OID
from ....database.mongo import get_collection
from ....exception.error_code import ObjectIdInvalid
from ..config import SENTENCE_COLLECTION
from ..models.sentence import (
    SentenceInCreate,
    SentenceInDB,
    SentenceInUpdate
)
from ..exception import (
    SentenceNotFound,
    SentenceExists
)


def generate_query(
    tags: Optional[List[str]] = None,
    strict_match: Optional[bool] = True,
    attribution: Optional[str] = None
) -> dict:
    '''创建查询条件'''
    quary = {}

    if tags is not None:
        quary.update({
            'tags': {f'${"all" if strict_match else "in"}': tags}
        })

    if attribution is not None:
        quary.update({'attribution': attribution})

    return quary


async def _get_sentence(quary: dict) -> SentenceInDB:
    collection = get_collection(SENTENCE_COLLECTION)
    result = await collection.find_one(quary)

    if result is None:
        raise SentenceNotFound

    return SentenceInDB.load_data(result)


async def get_sentence(**kwargs) -> SentenceInDB:
    '''查询单个句子'''
    quary = generate_query(**kwargs)
    return await _get_sentence(quary)


async def get_sentence_by_id(sentence_id: OID) -> SentenceInDB:
    '''通过id获取句子'''
    if not ObjectId.is_valid(sentence_id):
        raise ObjectIdInvalid('sentence_id')
    return await _get_sentence({'_id': ObjectId(sentence_id)})


async def _get_many_sentence(quary: dict, **kwargs):
    collection = get_collection(SENTENCE_COLLECTION)
    cursor = collection.find(
        quary, **kwargs
    ).sort('create_time', DESCENDING)

    data = []
    async for documents in cursor:
        data.append(SentenceInDB.load_data(documents))
    return data


async def get_sentences(limit: int, skip: int, **kwargs):
    '''查询多个句子'''
    quary = generate_query(**kwargs)
    return await _get_many_sentence(quary, limit=limit, skip=skip)


async def search_sentences(kw: str, limit: int, skip: int):
    '''通过关键词查询句子'''
    kw = findall(r'[^\s\+]+', kw)
    return await _get_many_sentence(
        {'$or': [{'sentence': {'$regex': k}} for k in kw]},
        limit=limit,
        skip=skip
    )


async def create_sentence(sentence: SentenceInCreate) -> SentenceInDB:
    '''创建新的句子'''
    collection = get_collection(SENTENCE_COLLECTION)
    try:
        result = await collection.insert_one(sentence.to_dict())
    except DuplicateKeyError:
        raise SentenceExists
    return SentenceInDB.load_data(
        {'_id': result.inserted_id, **sentence.to_dict()}
    )


async def update_sentence(
    sentence_id: OID,
    sentence: SentenceInUpdate
) -> SentenceInDB:
    '''更新句子'''
    collection = get_collection(SENTENCE_COLLECTION)
    result = await collection.find_one_and_update(
        {'_id': ObjectId(sentence_id)},
        {'$set': sentence.to_dict()},
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise SentenceNotFound
    return SentenceInDB.load_data(result)


async def delete_sentence(sentence_id: OID) -> SentenceInDB:
    '''删除句子'''
    collection = get_collection(SENTENCE_COLLECTION)
    result = await collection.find_one_and_delete(
        {'_id': ObjectId(sentence_id)},
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise SentenceNotFound
    return SentenceInDB.load_data(result)
