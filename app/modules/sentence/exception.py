#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-26 23:19:13
LastEditor: BATU1579
LastTime: 2021-12-27 11:33:42
FilePath: \\app\\modules\\sentence\\exception.py
Description: 一言api异常
'''
from ...exception.error_code import (
    resource_not_found,
    resource_exists,
    field_invalid
)


SentenceNotFound = resource_not_found('Sentence')

SentenceExists = resource_exists('Sentence')

TagInvalid = field_invalid(
    'tags',
    (
        'tags can only contain chinese characters letters, numbers.'
        'but not only numbers.'
    )
)
