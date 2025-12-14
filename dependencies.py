from models import db
from sqlalchemy.orm import sessionmaker

#criar sessao no bd e dar como parametro nas rotas
def pegar_sessao():  
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
        session.close
    finally:
        session.close()