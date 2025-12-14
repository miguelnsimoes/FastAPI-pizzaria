from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_contex

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
async def criar_conta(email: str, senha: str, nome:str, session = Depends(pegar_sessao)): #variavel session vem da dependencies.py
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        #ja existe um usuario com esse email
        return{
            "mensagem": "ja existe um usuario com esse"
        }
    else:
        senha_criptografada = bcrypt_contex.hash(senha)
        novo_usuario = Usuario(nome, email, senha_criptografada, True)
        session.add(novo_usuario)
        session.commit()
        return{
            "mensagem": "usuario cadastrado com sucesso"
        }