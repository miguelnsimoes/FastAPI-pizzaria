from models import db
from sqlalchemy.orm import sessionmaker

#criar sessao no bd e dar como parametro nas rotas
def pegar_sessao():  
    Session = sessionmaker(bind=db)
    session = Session()
    return session