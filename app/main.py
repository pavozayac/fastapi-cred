from fastapi import FastAPI
from .routers import auth, personal, income
from .db.database import engine
from .db.models import Base

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(
    auth.router,
    prefix='/auth',
    tags=['auth']
)

app.include_router(
    personal.router,
    prefix='/personal',
    tags=['personal']
)

app.include_router(
    income.router,
    prefix='/income',
    tags=['income']
)

@app.get('/')
async def root():
    return {
        'message': 'Welcome to the API root!'
    }