#!/usr/bin/env python3
"""
  POST: to create data.
   GET: to read data.
   PUT: to update data.
DELETE: to delete data.
"""
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

api = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@api.get("/")
def root():
    return {"Hello": "World"}


@api.get("/items/{item_id}")
def get_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@api.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item.price": item.price, "item_id": item_id}
