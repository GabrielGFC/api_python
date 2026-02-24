import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import usuarios


load_dotenv()

app = FastAPI(title="API de Usuários com Perfil")


raw_origins = os.getenv("CORS_ORIGINS", "*")
origins = [origin.strip() for origin in raw_origins.split(",")] if raw_origins else ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

