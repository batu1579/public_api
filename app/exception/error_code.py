#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-22 14:40:50
LastEditor: BATU1579
LastTime: 2021-12-22 22:07:49
FilePath: \\app\\exception\\error_code.py
Description: 服务器错误码
'''
from typing import Optional, Union
from pydantic import BaseModel, HttpUrl
from fastapi import HTTPException, status


class ErrorModel(BaseModel):
    code: str  # 错误码
    info: Optional[Union[str, HttpUrl]] = None  # 错误码对应的文档
    msg: str  # 错误详细信息


def resource_not_found(resource_name: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrorModel(
            code=404,
            info=None,
            msg=f'{resource_name} not found.'
        )
    )


def resource_exists(resource_name: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=ErrorModel(
            code=409,
            info=None,
            msg=f'{resource_name} already exists'
        )
    )


def ObjectIdInvalid(arg_name: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorModel(
            code=400,
            info=None,
            msg=(
                f'{arg_name} needs to be a ObjectId, it must be'
                f' a 12-byte input or a 24-character hex string'
            )
        )
    )
