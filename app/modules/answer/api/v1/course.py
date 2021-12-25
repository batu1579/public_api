#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-20 18:13:12
LastEditor: BATU1579
LastTime: 2021-12-25 14:18:21
FilePath: \\app\\modules\\answer\\api\\v1\\course.py
Description: 答案api课程接口
'''
from fastapi import APIRouter, Form, Path, Query
from typing import Optional
from bson import ObjectId

from ...crud.course import (
    get_course_by_name,
    get_course_by_id,
    get_many_course,
    create_course,
    update_course,
    search_courses,
    update_course_chapters
)
from ...crud.del_course import (
    delete_course,
    delete_course_chapters
)
from ...models.course import (
    CourseInResponse,
    ManyCourseInResponse,
    CourseInCreate,
    CourseInUpdate,
    Chapters
)
from ...field import (
    course_field,
    chapters_field,
    search_course_kw_field
)
from .....models.object_id import OID
from .....utils.response import response_success
from .....exception.error_code import ObjectIdInvalid
from .....utils.field import (
    id_field,
    limit_field,
    offset_field,
    description_field
)


router = APIRouter(tags=['课程操作'])


@router.get('/course/{course}')
async def get_course(
    course: Optional[str] = Path(..., **course_field)
):
    '''通过课程名称获取单个课程信息'''
    course = await get_course_by_name(course)
    return response_success(
        data=CourseInResponse(course=course)
    )


@router.get('/course/id/{course_id}')
async def _get_course_by_id(
    course_id: Optional[str] = Path(..., **id_field)
):
    '''通过id获取课程信息'''
    if not ObjectId.is_valid(course_id):
        raise ObjectIdInvalid('course_id')
    course = await get_course_by_id(OID(course_id))
    return response_success(
        data=CourseInResponse(course=course)
    )


@router.get('/courses')
async def get_courses(
    limit: Optional[int] = Query(**limit_field),
    offset: Optional[int] = Query(**offset_field)
):
    '''获取课程列表'''
    courses = await get_many_course(limit=limit, skip=offset)
    return response_success(
        data=ManyCourseInResponse(courses=courses)
    )


@router.get('/courses/search')
async def _search_courses(
    kw: Optional[str] = Query(..., **search_course_kw_field),
    limit: Optional[int] = Query(**limit_field),
    offset: Optional[int] = Query(**offset_field)
):
    '''搜索有关键词匹配的课程'''
    courses = await search_courses(kw, limit=limit, skip=offset)
    return response_success(
        data=ManyCourseInResponse(courses=courses)
    )


@router.post('/course')
async def create_new_course(
    course_name: str = Form(..., **course_field),
    description: str = Form(..., **description_field)
):
    '''创建新的课程'''
    course = CourseInCreate(
        course_name=course_name,
        description=description
    )
    course = await create_course(course)
    return response_success(
        data=CourseInResponse(course=course)
    )


@router.put('/course/{course_name}')
async def _update_course(
    course_name: Optional[str] = Path(..., **course_field),
    new_course_name: Optional[str] = Form(None, **course_field),
    description: Optional[str] = Form(None, **description_field)
):
    '''更新课程信息'''
    if new_course_name == description and (description is None):
        return response_success(
            msg="Why do you want to update without new data?"
        )
    course_data = CourseInUpdate(
        course_name=new_course_name,
        description=description
    )
    course = await update_course(course_name, course_data)
    return response_success(
        data=CourseInResponse(course=course)
    )


@router.delete('/course/{course_name}')
async def _delete_course(
    course_name: Optional[str] = Path(..., **course_field)
):
    '''删除课程'''
    course = await delete_course(course_name)
    return response_success(
        data=CourseInResponse(course=course)
    )


@router.get('/course/{course_name}/chapter')
async def _get_course_chapter(
    course_name: Optional[str] = Path(..., **course_field)
):
    '''获取课程的章节'''
    course = await get_course_by_name(course_name)
    return response_success(
        data=Chapters(chapter=course.chapter)
    )


@router.put('/course/{course_name}/chapter')
async def update_chapters(
    course_name: Optional[str] = Path(..., **course_field),
    chapter: Chapters = Form(..., **chapters_field)
):
    '''更新指定课程的章节列表'''
    course = await update_course_chapters(course_name, chapter.chapter)
    return response_success(
        data=CourseInResponse(course=course)
    )


@router.delete('/course/{course_name}/chapter')
async def delete_chapters(
    course_name: Optional[str] = Path(..., **course_field),
    chapter: Optional[Chapters] = Form(..., **chapters_field)
):
    '''删除课程的部分章节'''
    course = await delete_course_chapters(course_name, chapter.chapter)
    return response_success(
        data=CourseInResponse(course=course)
    )
