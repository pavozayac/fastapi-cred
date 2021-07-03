from fastapi.exceptions import HTTPException
from passlib.utils.decor import deprecated_function
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends
from ..schemas import User, UserIn, TokenResponse, LoginSchema
from ..db import models
from ..dependencies import Database
from passlib.context import CryptContext
from ..settings import SECRET_KEY
import datetime
from jose import jwt

router = APIRouter()

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_JWT(claims: dict):
    target = claims.copy()
    target.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})

    token = jwt.encode(target, SECRET_KEY)

    return token


@router.post('/register')
def register_user(user: UserIn, db: Session = Depends(Database)):
    dict = user.dict()
    dict['password'] = pass_context.hash(user.password)
    new_user = models.User(
        **dict
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #return new_user

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
    
