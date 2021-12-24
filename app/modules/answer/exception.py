#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-11-30 09:29:34
LastEditor: BATU1579
LastTime: 2021-12-24 10:06:51
Description: 答案api异常
'''
from ...exception.error_code import (
    resource_exists,
    resource_not_found,
    field_invalid
)


CourseNotFound = resource_not_found('Course')
CourseExists = resource_exists('Course')

ChapterNotFound = resource_not_found('Chapter')

AnsNotFound = resource_not_found('Answer')
AnsExists = resource_exists('Answer')

ChapterNameInvalid = field_invalid(
    arg_name='chapter',
    except_info=(
        'It can contain only 4 to 30'
        'Chinese or English characters or numbers'
    )
)

AnswerInvalid = field_invalid(
    arg_name='answer',
    except_info=(
        'It can not contain $'
    )
)
