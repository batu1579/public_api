#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-10 20:37:11
LastEditor: BATU1579
LastTime: 2021-12-22 22:09:01
Description: 公共异常
'''
from fastapi import HTTPException, status

from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from ..utils.response import response_error
from .error_code import ErrorModel


# --------------------------exception handler-------------------------------

async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError) -> JSONResponse:
    return response_error(
        error=ErrorModel(
            code=400,
            info=None,
            msg='The request arguments are invalid'
        ),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    # {
    #     'detail': exc.errors(),
    #     'body': exc.body
    # }


async def http_exception_handler(
        request: Request,
        exc: HTTPException) -> JSONResponse:
    return response_error(
        error=exc.detail,
        status_code=exc.status_code
    )


async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    return response_error(
        error=ErrorModel(
            code=500,
            info='Please contact administrator to report this error',
            msg='Unknown server error occurred'
        ),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
