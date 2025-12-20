from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

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

@rota_pedido.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin == False:
        raise HTTPException(status_code=401, detail="voce nao tem autorizacao para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all()
        return{
            "pedidos": pedidos
        }
    
@rota_pedido.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, 
                                item_pedido_schema: ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao), 
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="voce nao tem autorizacao para fazer essa operação")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, item_pedido_schema.id_pedido)
    pedido.calcular_preco()
    session.add(item_pedido)
    session.commit()
    return{
        "mensagem": "item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedio": pedido.preco
    }