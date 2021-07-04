from fastapi import FastAPI
from .routers import auth, personal, income, obligation, identity
from .db.database import engine
from .db.models import Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:63601"
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

app.include_router(
    obligation.router,
    prefix='/obligation',
    tags=['obligation']
)
app.include_router(
    identity.router,
    prefix='/identity',
    tags=['identity']
)

@app.get('/')
async def root():
    return {
        'message': 'Welcome to the API root!'
    }