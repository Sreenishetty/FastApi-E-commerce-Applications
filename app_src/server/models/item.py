from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)

    class Config:
        schema_extra = {
            "example" : {
                "title": "Any kind of items from shopping can be added",
                "content": "some content about the item"
            }
        }

class UserSchema(BaseModel):
    name : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        schema_extra = {
            "example":{
                "name" : "sreeni",
                "email": "sreeni@123.com",
                "password": "123"
            }
        }

class UserLoginSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        schema_extra = {
            "example":{
                "email": "sreeni@123.com",
                "password": "123"
            }

        }


class Item(BaseModel):
    item_name: str= Field(...)
    price: float= Field(...)
    qty: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "item_name": "Item Name",
                "price": 0.00,
                "qty": 0.000
            }
        }


class Quanity(BaseModel):
    qty: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "qty": 0.000
            }
        }

class Updated_Item(BaseModel):
    item_name: str= Field(...)
    price: float= Field(...)
    qty: float = Field(...)


    class Config:
        schema_extra = {
            "example": {
                "item_name": "Item Name",
                "price": 00.00,
                "qty": 0.00,
                "Grades of Item ": { "A": 5, "B": 5, "C": 3 }
            }
        }

class Payment_mtd(BaseModel):
    payment_methods: str= Field(...)
    transaction_id: str = Field(...)
    # available_amount:float = Field(...)
    card_no:str =Field(...)
    card_status:str=Field(...)
    cvv:str=Field(...)

    class Config:
        schema_extra = {
            "example":{
                "payment_methods": "visa",
                "transaction_id":"id",
                # "available_amount":0.000,
                "card_no": "2312213312XXXTD",
                "card_status": "Active",
                "cvv":"321"
            }
        }

class Address_mtd(BaseModel):
    customer_name: str= Field(...)
    address: str = Field(...)
    city:str = Field(...)
    region:str =Field(...)
    country:str=Field(...)
    pincode: float=Field(...)

    class Config:
        schema_extra = {
            "example":{
                "customer_name": "Name of the customer",
                "address":"customer_address",
                "city":"city name",
                "region": "current region",
                "country": "country name",
                "pincode": 0.000
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": "item added successfully.",
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}