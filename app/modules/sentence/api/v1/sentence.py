#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-27 10:32:15
LastEditor: BATU1579
LastTime: 2021-12-27 13:12:34
FilePath: \\app\\modules\\sentence\\api\\v1\\sentence.py
Description: 一言api句子接口
'''
from fastapi import APIRouter, Form, Path, Query
from typing import Optional
from bson import ObjectId

from .....utils.response import response_success
from .....utils.field import (
    id_field,
    limit_field,
    offset_field
)
from ...curd.sentence import (
    get_sentence,
    get_sentence_by_id,
    get_sentences,
    search_sentences,
    create_sentence,
    update_sentence,
    delete_sentence
)
from ...models.sentence import (
    Tags,
    SentenceInUpdate,
    SentenceInCreate,
    SentenceInResponse,
    ManySentenceInResponse
)
from ...field import (
    sentence_field,
    attribution_field,
    tags_field,
    strict_match_field,
    search_sentence_kw_field
)


router = APIRouter(tags=['句子操作'])


@router.get('/sentence')
async def _get_sentence(
    sentence_tags: Optional[Tags] = Form(None, **tags_field),
    strict_match: Optional[bool] = Form(True, **strict_match_field),
    attribution: Optional[str] = Form(None, **attribution_field)
):
    '''获取单个句子'''
    sentence = await get_sentence(
        tags=sentence_tags.tags,
        strict_match=strict_match,
        attribution=attribution
    )
    return response_success(
        data=SentenceInResponse(sentence=sentence)
    )


@router.get('/sentence/id/{sentence_id}')
async def _get_sentence_by_id(
    sentence_id: Optional[str] = Path(..., **id_field)
):
    '''通过id获取句子'''
    sentence = await get_sentence_by_id(sentence_id)
    return response_success(
        data=SentenceInResponse(sentence=sentence)
    )


@router.get('/sentences')
async def _get_sentences(
    sentence_tags: Optional[Tags] = Form(None, **tags_field),
    strict_match: Optional[bool] = Form(True, **strict_match_field),
    attribution: Optional[str] = Form(None, **attribution_field),
    limit: Optional[int] = Query(**limit_field),
    offset: Optional[int] = Query(**offset_field)
):
    '''获取多个句子'''
    sentences = await get_sentences(
        limit, offset,
        tags=sentence_tags.tags,
        strict_match=strict_match,
        attribution=attribution
    )
    return response_success(
        data=ManySentenceInResponse(sentences=sentences)
    )


@router.get('/sentences/search')
async def _search_sentences(
    kw: Optional[str] = Query(None, **search_sentence_kw_field),
    limit: Optional[int] = Query(**limit_field),
    offset: Optional[int] = Query(**offset_field)
):
    '''通过关键词查询句子'''
    sentences = await search_sentences(kw=kw, limit=limit, skip=offset)
    return response_success(
        data=ManySentenceInResponse(sentences=sentences)
    )


@router.post('/sentence')
async def _create_sentence(
    sentence: Optional[str] = Form(..., **sentence_field),
    attribution: Optional[str] = Form('佚名', **attribution_field),
    sentence_tags: Optional[Tags] = Form(..., **tags_field),
):
    '''新建句子'''
    sentence = SentenceInCreate(
        sentence=sentence,
        attribution=attribution,
        tags=sentence_tags.tags
    )
    sentence = await create_sentence(sentence)
    return response_success(
        data=SentenceInResponse(sentence=sentence)
    )


@router.put('/sentence/id/{sentence_id}')
async def _update_sentence(
    sentence_id: Optional[str] = Path(..., **id_field),
    sentence: Optional[str] = Form(None, **sentence_field),
    attribution: Optional[str] = Form(None, **attribution_field),
    sentence_tags: Optional[Tags] = Form(None, **tags_field)
):
    '''更新句子'''
    sentence = SentenceInUpdate(
        sentence=sentence,
        attribution=attribution,
        tags=sentence_tags.tags
    )
    sentence = await update_sentence(ObjectId(sentence_id), sentence)
    return response_success(
        data=SentenceInResponse(sentence=sentence)
    )


@router.delete('/sentence/id/{sentence_id}')
async def _delete_sentence(
    sentence_id: Optional[str] = Path(..., **id_field)
):
    '''删除句子'''
    sentence = delete_sentence(sentence_id)
    return response_success(
        data=SentenceInResponse(sentence=sentence)
    )
