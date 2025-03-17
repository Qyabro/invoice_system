from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()

# Se incluyen rutas desde routes.py
app.include_router(router)
