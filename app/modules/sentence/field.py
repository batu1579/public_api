#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-26 23:19:23
LastEditor: BATU1579
LastTime: 2021-12-27 12:57:14
FilePath: \\app\\modules\\sentence\\field.py
Description: 一言api的字段检查
'''
from ...utils.field import search_kw_field


sentence_field = {
    'min_length': 2,
    'max_length': 100,
    'description': '一言的句子，什么都可以写。但是不许写垃圾话昂!',
    'example': '超凡的思想是不会与凡夫俗子共存的。',
    'regex': r'^[^\$]+$'
}

attribution_field = {
    'min_length': 2,
    'max_length': 50,
    'description': '句子对应的出处，如果出自作品的话可以用书名号括起来',
    'example': '《最长的一天》',
    'regex': r'^[^\$]+$'
}

tags_field = {
    'description': (
        '句子的标签，不用关心是不是存在，因为获取的时候是直接查询的。'
        '用来给句子分类，一个句子可以有多个标签，随你分类。'
        '但是拜托别把两个相对的标签放进同一个句子里hhhh'
    ),
    'example': '搞笑',
}

strict_match_field = {
    'description': '强制匹配所有标签，默认为真',
    'example': False
}

search_sentence_kw_field = {
    'regex': r'^[\u4e00-\u9fa5a-zA-Z0-9\+\s]+$',
    **search_kw_field
}
