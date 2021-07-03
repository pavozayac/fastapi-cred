from fastapi import FastAPI
from .routers import auth
from .db.database import engine
from .db.models import Base

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(
    auth.router,
    prefix='/auth',
    tags=['auth']
)

@app.get('/')
async def root():
    return {
        'message': 'Welcome to the API root!'
    }