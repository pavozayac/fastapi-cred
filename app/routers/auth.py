from typing import Optional
from fastapi.exceptions import HTTPException
from passlib.utils.decor import deprecated_function
from sqlalchemy import schema
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends, Header
from ..schemas import User, UserIn, TokenResponse, LoginSchema
from ..db import models
from ..dependencies import Database, Authenticated
from passlib.context import CryptContext
from ..settings import SECRET_KEY
import datetime
from jose import jwt
import uuid

router = APIRouter()

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_JWT(claims: dict):
    target = claims.copy()
    target.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})

    token = jwt.encode(target, SECRET_KEY)

    return token


@router.post('/register', response_model=User)
def register_user(user: UserIn, db: Session = Depends(Database)):
    email_check = db.query(models.User).filter(models.User.email == user.email).first()
    
    if email_check is not None:
        raise HTTPException(409, 'This email is already registered')

    user_dict = user.dict()
    user_dict['password'] = pass_context.hash(user.password)
    user_dict['uuid'] = str(uuid.uuid1())
    new_user = models.User(
        **user_dict
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post('/login', response_model=TokenResponse)
def login_user(login: LoginSchema, db: Session = Depends(Database)):
    user = db.query(models.User).filter(models.User.email == login.email).first()

    if user is None:
        raise HTTPException(404, 'Could not login with this email')

    if not pass_context.verify(login.password, user.password):
        raise HTTPException(401, 'Invalid credentials')

    token = create_JWT({
        'email': login.email
    })

    return TokenResponse(
        token = token,
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    )
    
@router.get('/user-by-uuid', response_model=User)
async def get_user_by_id(uuid: Optional[str] = Header(None), db: Session = Depends(Database)):
    if uuid is None:
        raise HTTPException(401)

    user = db.query(models.User).filter(models.User.uuid == uuid).first()

    if user is None:
        raise HTTPException(404)
    
    return user

@router.get('/uuid')
async def get_uuid(user: models.User = Depends(Authenticated)):
    return {
        'identifier': user.uuid
    }

@router.get('/current', response_model=User)
async def get_current_user(user: models.User = Depends(Authenticated)):
    return user