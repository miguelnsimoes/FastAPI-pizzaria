from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario

rota_pedido = APIRouter(prefix="/pedidos", tags=["pedido"], dependencies=[Depends(verificar_token)])

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

@rota_pedido.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="voce nao tem autorizacao para fazer essa modificacao")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido {id_pedido} cancelado com sucesso",
        "pedido": pedido
    }