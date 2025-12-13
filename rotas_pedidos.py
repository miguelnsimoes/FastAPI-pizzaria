from fastapi import APIRouter

rota_pedido = APIRouter(prefix="/pedidos", tags=["pedido"])

@rota_pedido.get("/")
async def pedidos():
    """
    ROTA PADRAO DE PEDIDOS DO NOSSO SISTEMA
    """
    return {
        "mensagem": "voce acessou a rota de pedidos"
    }