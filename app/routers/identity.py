from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from ..dependencies import Database, Authenticated, UserByUUID
from ..db import models
from ..schemas import IdentityCard, IdentityCardIn

router = APIRouter()

@router.post('/')
async def post_identity_card(card: IdentityCardIn, user: models.User = Depends(Authenticated), db: Session = Depends(Database)):
    new_identity_card = models.IdentityCard(
        user_id = user.id,
        **card.dict()
    )

    db.add(new_identity_card)
    db.commit()
    db.refresh(new_identity_card)

    return new_identity_card

@router.get('/', response_model=IdentityCard)
async def get_identity_card(user: models.User = Depends(Authenticated)):
    card = user.identity_card
    print(str(card))
    if card is None: 
        raise HTTPException(404)
    return card

@router.get('/external')
async def get_identity_card_by_uuid(user: models.User = Depends(UserByUUID)):
    card = user.identity_card
    if card is None: 
        raise HTTPException(404)
    return card