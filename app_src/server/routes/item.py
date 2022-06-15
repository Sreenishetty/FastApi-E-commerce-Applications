from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database import (
    add_item,
    delete_item,
    retrieve_item,
    retrieve_items,
    update_item,
)
from models.item import (
    Item,
    Updated_Item
)

router = APIRouter()