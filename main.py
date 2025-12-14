from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

bcrypt_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")

from rotas_auth import rota_auth
from rotas_pedidos import rota_pedido

app.include_router(rota_auth)
app.include_router(rota_pedido)