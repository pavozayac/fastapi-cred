from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from ..db import models
from ..schemas import Obligation, ObligationIn
from ..dependencies import Authenticated, Database, UserByUUID
from typing import List

router = APIRouter()

@router.post('/', response_model=Obligation)
async def post_obligation(obligation: ObligationIn, user: models.User = Depends(Authenticated), db: Session = Depends(Database)):
    new_obligation = models.Obligation(
        user_id = user.id,
        **obligation.dict()
    )

    db.add(new_obligation)
    db.commit()
    db.refresh(new_obligation)

    return new_obligation

@router.get('/', response_model=List[Obligation])
async def get_obligations(user: models.User = Depends(Authenticated)):
    return user.obligations

@router.get('/external', response_model=List[Obligation])
async def get_obligation_external(user: models.User = Depends(UserByUUID)):
    return user.obligations