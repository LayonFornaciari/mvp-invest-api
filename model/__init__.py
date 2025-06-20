from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.investimento import Investimento, TipoInvestimento

# O caminho para o diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# Define a pasta para o banco de dados
db_dir = os.path.join(basedir, 'database')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# O caminho para o arquivo do banco de dados
db_path = os.path.join(db_dir, 'database.db')


# url de acesso ao banco (essa é uma configuração do SQLAlchemy)
db_url = 'sqlite:///%s' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de sessão com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)