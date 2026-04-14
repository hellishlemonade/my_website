from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.post import router as post_router


app = FastAPI()


app.include_router(router=auth_router)
app.include_router(router=post_router)
