#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 17:42:30
LastEditor: BATU1579
LastTime: 2021-12-22 22:04:01
Description: 设置app对象(加载中间件和路由)
'''
import time

from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from fastapi.exceptions import RequestValidationError, HTTPException

from .modules.api_router import public_api_router
from .config import ORIGINS
from .database.utils import connect_to_db, close_connection

from .exception.handler import (
    validation_exception_handler,
    http_exception_handler,
    error_handler
)

app = FastAPI(
    title="batu1579.com的公共api",
    description="公共api文档",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redocs"
)

# 中间件

# 开启cors（跨源资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 开启gzip压缩
app.add_middleware(
    GZipMiddleware,
    minimum_size=500  # 500字节以上
)


# 记录处理时间
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 只接受https请求，将http请求重定向到https
# app.add_middleware(HTTPSRedirectMiddleware)

# 注册路由
app.include_router(public_api_router)

# 注册事件
app.add_event_handler('startup', connect_to_db)
app.add_event_handler('shutdown', close_connection)

# 注册异常处理
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, error_handler)
