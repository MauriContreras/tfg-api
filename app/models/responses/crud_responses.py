# -*- coding: utf-8 -*-
"""
    Python Script

    @author: Mauricio Contreras Garay
    @version: 0.1
"""
import uuid

from pydantic import BaseModel
from pydantic import create_model

class NotFound(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Person not found."},
        }


class ItemCreated(BaseModel):
    detail: str = "Item created"

    class Config:
        schema_extra = {
            "example": {"detail": "Item created"},
        }


class ItemUpdated(BaseModel):
    detail: str = "Item updated"

    class Config:
        schema_extra = {
            "example": {"detail": "Item updated"},
        }


class ItemDeleted(BaseModel):
    detail: str = "Item deleted"

    class Config:
        schema_extra = {
            "example": {"detail": "Item deleted"},
        }


class ResponseModelTemplate(BaseModel):
    code: int = 200
    message: str

    #Dynamical generation of classe in python
    '''
    pydantic.create_model(name: str, **field_definitions) -> Type[pydantic.main.BaseModel]
    name: an unique identifier
    **field_definitions: fields that you want to add to the dynamically created model.
    Each field is specified as a keyword argument, key -> field name & value -> type 
    
    '''
    @classmethod
    def add_fields(cls, **field_definitions):
        return create_model(uuid.uuid4().hex, __base__=cls, **field_definitions)


