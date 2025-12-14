from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_contex
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

rota_auth = APIRouter(prefix="/auth", tags=["auth"])

@rota_auth.get("/")
async def autenticar():
    """
        ROTA PADRAO DE AUTENTICACAO DO NOSSO SISTEMA
    """
    return{
        "mensagem": "voce acessou a rota padrao de autenticacao",
        "autenticado": False
    }

@rota_auth.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)): #variavel session vem da dependencies.py
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="email do usuario ja cadastrado") 
    else:
        senha_criptografada = bcrypt_contex.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return{
            "mensagem": f"usuario cadastrado com sucesso {usuario_schema.email}"
        }