from typing import Optional, List
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends

from sqlalchemy.orm.session import Session
from sqlalchemy.sql.coercions import expect
from .db.database import SessionLocal
from .db import models
from fastapi import Header
from jose import jwt
from .settings import SECRET_KEY

def Database():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def Authenticated(Authentication: Optional[str] = Header(None), db: Session = Depends(Database)) -> models.User:
    if Authentication is None:
        raise HTTPException(401, 'Bruh')
    
    try:
        payload = jwt.decode(Authentication, SECRET_KEY, algorithms=['HS256'])
        email = payload.get('email')

        if email is None:
            raise HTTPException(401)
        
    except jwt.JWTError:
        raise HTTPException(401)

    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None: 
        raise HTTPException(401)

    return user

def UserByUUID(uuid: Optional[str] = Header(None), db: Session = Depends(Database)) -> models.User:
    if uuid is None:
        raise HTTPException(401)

    user = db.query(models.User).filter(models.User.uuid == uuid).first()

    if user is None:
        raise HTTPException(401)

    return user