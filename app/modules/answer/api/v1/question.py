#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-20 18:13:24
LastEditor: BATU1579
LastTime: 2021-12-25 14:18:41
FilePath: \\app\\modules\\answer\\api\\v1\\question.py
Description: 答案api问题接口
'''
from fastapi import APIRouter, Form, Path, Query
from typing import Optional
from bson import ObjectId

from ...crud.course import get_course_id
from ...crud.question import (
    get_ans_by_question,
    get_ans_by_question_id,
    get_ans_by_chapter,
    get_ans_by_regex,
    create_question,
    update_question,
    delete_question,
    delete_question_by_id
)
from ...field import (
    course_field,
    chapter_field,
    question_field,
    answer_field,
    search_question_kw_field
)
from ...models.question import (
    QuestionInCreate,
    QuestionInUpdate,
    QuestionInResponse,
    ManyQuestionsInResponse,
    DetailQuestionInResponse,
    Answer
)
from .....utils.response import response_success
from .....models.object_id import OID
from .....utils.field import (
    limit_field,
    offset_field,
    id_field
)


router = APIRouter(tags=['答案操作'])


@router.get('/question/{question}')
async def get_ans(
    question: Optional[str] = Path(..., **question_field)
):
    '''获取正则匹配的第一个问题答案'''
    ans = await get_ans_by_question(question)
    return response_success(data=QuestionInResponse(question=ans))


@router.get('/question/id/{question_id}')
async def _get_ans_by_id(
    question_id: Optional[str] = Path(..., **id_field)
):
    '''通过问题id获取问题答案'''
    ans = await get_ans_by_question_id(question_id)
    return response_success(data=QuestionInResponse(question=ans))


@router.get('/{course_name}/{chapter}/questions')
async def get_chapter_ans(
    course_name: Optional[str] = Path(..., **course_field),
    chapter: Optional[str] = Path(..., **chapter_field)
):
    '''获取整个章节的答案'''
    anses = await get_ans_by_chapter(course_name, chapter)
    return response_success(data=ManyQuestionsInResponse(questions=anses))


@router.get('/questions/search')
async def search_ans(
    kw: Optional[str] = Query(..., **search_question_kw_field),
    limit: Optional[int] = Query(**limit_field),
    offset: Optional[int] = Query(**offset_field)
):
    '''通过正则表达式查询答案'''
    anses = await get_ans_by_regex(kw, limit, offset)
    return response_success(data=ManyQuestionsInResponse(questions=anses))


@router.post('/question')
async def _create_question(
    question: Optional[str] = Form(..., **question_field),
    answer: Optional[Answer] = Form(..., **answer_field),
    course_name: Optional[str] = Form(..., **course_field),
    chapter: Optional[str] = Form(..., **chapter_field)
):
    course_id = await get_course_id(course_name)
    que_obj = QuestionInCreate(
        question=question,
        answer=answer.answer,
        course=ObjectId(course_id),
        chapter=chapter
    )
    '''创建新的问题和答案'''
    result = await create_question(course_name, que_obj)
    return response_success(data=DetailQuestionInResponse(question=result))


@router.put('/question/id/{question_id}')
async def _update_question(
    question_id: Optional[str] = Path(..., **id_field),
    question: Optional[str] = Form(None, **question_field),
    answer: Optional[Answer] = Form(None, **answer_field),
    course_name: Optional[str] = Form(None, **course_field),
    chapter: Optional[str] = Form(None, **chapter_field)
):
    if (question == answer == course_name == chapter and answer is None):
        return {"msg": "Why do you want to update without new data?"}
    que_obj = QuestionInUpdate(
        question=question,
        answer=answer.answer,
        course=None if course_name else await get_course_id(course_name),
        chapter=chapter
    )
    '''更改问题信息'''
    result = await update_question(question_id, que_obj)
    return response_success(data=DetailQuestionInResponse(question=result))


@router.delete('/question/{question}')
async def _delete_question(question: str):
    '''删除问题'''
    result = await delete_question(question)
    return response_success(data=DetailQuestionInResponse(question=result))


@router.delete('/question/id/{question_id}')
async def _delete_question_by_id(
    question_id: Optional[str] = Path(..., **id_field)
):
    '''删除指定id的问题'''
    result = await delete_question_by_id(OID(question_id))
    return response_success(data=DetailQuestionInResponse(question=result))
