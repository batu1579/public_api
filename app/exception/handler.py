#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-10 20:37:11
LastEditor: BATU1579
LastTime: 2021-12-22 15:15:02
Description: 公共异常
'''
from fastapi import HTTPException, status

from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


# --------------------------exception handler-------------------------------

async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            'detail': exc.errors(),
            'body': exc.body
        })
    )


async def http_exception_handler(
        request: Request,
        exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc)
    )
