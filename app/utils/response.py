#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2021-12-22 14:00:03
LastEditor: BATU1579
LastTime: 2021-12-22 21:04:54
FilePath: \\app\\utils\\response.py
Description: 统一接口返回格式
'''
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import Any

from bson import ObjectId
from datetime import datetime, timezone

from ..models.base_model import BaseMongoModel as BMM
from ..exception.error_code import ErrorModel


def response_success(data: Any = None, msg: str = 'Success') -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            obj={
                'status': 1,
                'msg': msg,
                'data': data.to_dict() if isinstance(data, BMM) else data
            },
            custom_encoder={
                ObjectId: lambda oid: str(oid),
                datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            }
        )
    )


def response_error(
        error: ErrorModel,
        status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({
            'status': -1,
            **error.dict()
        })
    )
