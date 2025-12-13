from fastapi import FastAPI

app = FastAPI()

from rotas_auth import rota_auth
from rotas_pedidos import rota_pedido

app.include_router(rota_auth)
app.include_router(rota_pedido)