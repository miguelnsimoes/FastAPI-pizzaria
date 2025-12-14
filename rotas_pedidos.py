from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

rota_pedido = APIRouter(prefix="/pedidos", tags=["pedido"])

@rota_pedido.get("/")
async def pedidos():
    """
    ROTA PADRAO DE PEDIDOS DO NOSSO SISTEMA
    """
    return {
        "mensagem": "voce acessou a rota de pedidos"
    }


@rota_pedido.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {
        "mensagem": f"pedido criado com sucesso. ID do pedido {novo_pedido.id}"
    }