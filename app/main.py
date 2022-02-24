from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import ad, category, user, auth
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
)

app.include_router(ad.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def hello():
    return {'message': 'Hello, world!'}