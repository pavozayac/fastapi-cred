from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from ..dependencies import Authenticated, Database, UserByUUID
from ..db import models
from ..schemas import IncomeSource, IncomeSourceIn
from typing import List

router = APIRouter()

@router.post('/', response_model=IncomeSource)
async def post_income_source(income: IncomeSourceIn, user: models.User = Depends(Authenticated), db: Session = Depends(Database)):
    new_income_source = models.IncomeSource(
        user_id = user.id,
        **income.dict()
    )

    db.add(new_income_source)
    db.commit()
    db.refresh(new_income_source)

    return new_income_source

@router.get('/', response_model=List[IncomeSource])
async def get_income_source(user: models.User = Depends(Authenticated)):
    return user.income_sources

@router.get('/external', response_model=List[IncomeSource])
async def get_income_source_by_uuid(user: models.User = Depends(UserByUUID)):
    return user.income_sources