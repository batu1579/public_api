#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 17:33:45
LastEditor: BATU1579
LastTime: 2021-12-21 08:15:57
Description: 启动服务器入口
'''
import uvicorn


if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        reload=True,
        host="0.0.0.0",
        port=8888,
    )
