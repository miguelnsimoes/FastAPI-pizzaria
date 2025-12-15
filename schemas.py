from pydantic import BaseModel
from typing import Optional #declada um parametro opcional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True #esse schema pode ser criado a partir de objetos e não so de dicionários

class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True