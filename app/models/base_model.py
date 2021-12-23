#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
Date: 2021-10-07 21:06:48
LastEditor: BATU1579
LastTime: 2021-12-23 16:22:38
Description: 基类
'''
import abc
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, BaseConfig, Field
from typing import Union, Optional

from .object_id import OID


class ReturnDict(metaclass=abc.ABCMeta):
    '''有特殊返回字典方法的数据类的抽象类'''
    @abc.abstractmethod
    def to_dict(self, **kwargs) -> dict: pass


class BaseMongoModel(BaseModel, ReturnDict):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }

    def to_dict(self):
        '''给所有类添加to_dict方法，统一调用'''
        return self.dict()


class InUpdateModel(BaseMongoModel, ReturnDict):
    '''
    继承时必须放在最前面
    '''
    def to_dict(self, **kwargs) -> dict:
        return self.data_filter(self.dict(**kwargs))

    def data_filter(self, data: dict) -> dict:
        '''
        数据过滤器
        删除掉为空的字段，只保留有更新的字段
        '''
        return {k: v for k, v in data.items() if v is not None}


class InDBModel(BaseMongoModel, ReturnDict):
    '''
    继承时必须放在最前面
    '''
    resource_id: OID = Field(default_factory=ObjectId)

    @classmethod
    def load_data(cls, data: dict) -> Union['InDBModel', dict]:
        '''把从数据库中获取的数据 _id 字段转换成 resource_id 字段'''
        if not data:
            return data
        data['resource_id'] = data.pop('_id', None)
        return cls(**data)

    def to_dict(self, **kwargs) -> dict:
        '''
        把模型类中的id字段转换成数据库中的主键 _id 字段
        '''
        fields = self.dict(**kwargs)
        if '_id' not in fields and 'resource_id' in fields:
            fields['_id'] = fields.pop('resource_id', None)
        return fields


class WithOwner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def remove_owner_field(self):
        '''
        去掉 owner_id 字段，返回一个不带 owner_id 的对应的 InDBModel
        '''
        pass


class CreateTime(BaseModel):
    create_time: Optional[datetime] = datetime.now()
