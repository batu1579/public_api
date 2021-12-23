#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-23 11:04:14
LastEditor: BATU1579
LastTime: 2021-12-23 15:15:12
FilePath: \\app\\utils\\field.py
Description: 参数校验
'''


# 0 < limit <:  50
limit_field = {
    'default': 10,
    'gt': 0,
    'le': 50,
    'description': '限制接口返回的数据条数，范围在0到50之间，默认为10'
}

# 0 < offset
offset_field = {
    'default': 0,
    'ge': 0,
    'description': '跳过文档的数量'
}

id_field = {
    'ge': 24,
    'le': 24,
    'regex': r'^[0-9a-zA-Z]{24}$',
    'description': '数据对应的ObjectId'
}

description_field = {
    'min_length': 0,
    'max_length': 100,
    'regex': r'^[^;\'\$\*\/\\\-]+$',
    'description': '对资源的详细描述'
}

# r'^[^;\'\$\*\/\\\-]+$' 谨防注入 :)
# r'^[\u4e00-\u9fa5\w()\-]+$' 更严格的防止注入，除了指定的符号其他都不能用
