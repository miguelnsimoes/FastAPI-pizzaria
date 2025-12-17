from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_contex, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

rota_auth = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": id_usuario, #sub é o identificador para o dono do token
        "exp": data_expiracao
    }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_contex.verify(senha, usuario.senha):
        return False
    return usuario

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
    
@rota_auth.post("/login")
async def login(login_schema: LoginSchema,  session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="usuario nao encontrado ou credenciais invalidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "acess_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
@rota_auth.get("/refresh")
async def usar_refresh_token(usuario: Usuario = Depends(verificar_token)):
    usuario = verificar_token(token)
    access_token = criar_token(usuario.id)
    return {
    "acess_token": access_token,
    "token_type": "Bearer"
}