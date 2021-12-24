#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-23 13:28:43
LastEditor: BATU1579
LastTime: 2021-12-24 12:17:23
FilePath: \\app\\modules\\answer\\field.py
Description: 答案api的字段检查
'''


course_field = {
    'min_length': 4,
    'max_length': 30,
    'description': (
        '课程（练习册）名称，保证能够通过这个名称找到唯一的课本或者课程'
        '每个名词之间用 \'-\' 连接'
        '大体格式为: <学业信息>-<课程信息>'
        '课本详细格式: <地区>-<学科>-<阶段>-<年级>-<书籍名称>-<版本>-<年份>'
        '网课详细格式: <APP名称>-<学科>-<课程全称>'
    ),
    'example': '北京-数学-初中-七年级上册-学探诊-人教版-2020',
    'regex': r'^[\u4e00-\u9fa5a-zA-Z0-9\-]+$'
}

chapters_field = {
    'description': (
        '课程中章节的名称，根据书中或软件中的分类填写，没有的话可以自己定。'
        '尽量保证格式相同，不能混用命名方式。'
        '不允许使用标点符号'
    ),
    'example': ['第一章', '第二章']
}

chapter_field = {
    'min_length': 1,
    'max_length': 10,
    'regex': r'^[\u4e00-\u9fa5a-zA-Z0-9]+$',
    **chapters_field
}

question_field = {
    'min_length': 1,
    'max_length': 100,
    'description': '题目全文，力求完整',
    'example': '计算机界的最高奖项是？',
    'regex': r'^[\$]$'
}

answer_field = {
    'description': (
        '题目答案,尽量记录答案内容，不以选项为答案，'
        '如果没有办法存储或者获取答案则存储选项，格式: Option[选项]'
    ),
    'example': [
        'Option[A]',
        '阿兰·图灵'
    ]
}
