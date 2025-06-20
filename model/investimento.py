from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# Tabela para os tipos de investimento (categorias)
class TipoInvestimento(Base):
    __tablename__ = 'tipo_investimento'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)

    def __init__(self, nome:str):
        """
        Cria um Tipo de Investimento

        Arguments:
            nome: o nome da categoria do investimento.
        """
        self.nome = nome

# Tabela principal para os investimentos
class Investimento(Base):
    __tablename__ = 'investimento'

    id = Column(Integer, primary_key=True)
    nome_ativo = Column("nome_ativo", String(100), nullable=False)
    quantidade = Column("quantidade", Float, nullable=False)
    valor_investido = Column("valor_investido", Float, nullable=False)
    data_compra = Column("data_compra", DateTime, default=datetime.now())

    # Definição do relacionamento entre o investimento e um tipo de investimento.
    # A tabela Investimento terá uma chave estrangeira para a tabela TipoInvestimento.
    tipo_id = Column(Integer, ForeignKey("tipo_investimento.id"), nullable=False)
    tipo = relationship("TipoInvestimento")

    def __init__(self, nome_ativo:str, quantidade:float, valor_investido:float,
                 tipo_id:int, data_compra:Union[DateTime, None] = None):
        """
        Cria um Investimento

        Arguments:
            nome_ativo: nome do ativo (ex: PETR4, Bitcoin).
            quantidade: quantidade de cotas/unidades do ativo.
            valor_investido: valor total pago pelo ativo.
            tipo_id: id da categoria do investimento.
            data_compra: data em que o investimento foi realizado.
        """
        self.nome_ativo = nome_ativo
        self.quantidade = quantidade
        self.valor_investido = valor_investido
        self.tipo_id = tipo_id
        if data_compra:
            self.data_compra = data_compra

    