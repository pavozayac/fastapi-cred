from typing import Optional
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from ..dependencies import Authenticated, Database, UserByUUID
from ..schemas import PersonalData, PersonalDataIn
from  ..db import models

router = APIRouter()

@router.post('/', response_model=PersonalData)
async def post_personal_data(personal: PersonalDataIn, user: models.User = Depends(Authenticated), db: Session = Depends(Database)):
    existing_check = db.query(models.PersonalData).filter(models.PersonalData.user_id == user.id).first()
    if existing_check is not None:
        raise HTTPException(409, 'Personal data already posted')

    new_personal = models.PersonalData(
        user_id = user.id,
        **personal.dict()
    )

    db.add(new_personal)
    db.commit()
    db.refresh(new_personal)

    return new_personal

@router.get('/', response_model=PersonalData)
async def get_personal_data(user: models.User = Depends(Authenticated)):
    retrieved = user.personal_data

    if retrieved is None:
        raise HTTPException(404, 'No personal data found')

    return retrieved

@router.get('/external', response_model=PersonalData)
async def get_personal_data_by_uuid(user: models.User = Depends(UserByUUID)):
    retrieved = user.personal_data

    if retrieved is None:
        raise HTTPException(404, 'No personal data found')

    return retrieved