from fastapi import APIRouter, Depends
from fastui import AnyComponent, FastUI

from app.models import User

from typing import Annotated

router = APIRouter()

@router.get('/login/', response_model=FastUI, response_model_exclude_none=True)
async def login():
    raise NotImplementedError