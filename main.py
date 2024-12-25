from fastapi import FastAPI
from auth import router as auth_router
from predictor import router as predictor_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(predictor_router)