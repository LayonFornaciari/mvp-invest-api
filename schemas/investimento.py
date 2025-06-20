from pydantic import BaseModel
from typing import List, Optional
from model.investimento import Investimento, TipoInvestimento


# Schemas para Tipo de Investimento
class TipoInvestimentoSchema(BaseModel):
    """ Define como um novo tipo de investimento a ser inserido deve ser representado
    """
    nome: str = "Ações"

class TipoInvestimentoViewSchema(BaseModel):
    """ Define como um tipo de investimento será retornado
    """
    id: int = 1
    nome: str = "Ações"

class ListagemTiposInvestimentoSchema(BaseModel):
    """ Define como uma listagem de tipos de investimento será retornada.
    """
    tipos_investimento:List[TipoInvestimentoViewSchema]


# Schemas para Investimento
class InvestimentoSchema(BaseModel):
    """ Define como um novo investimento a ser inserido deve ser representado
    """
    nome_ativo: str = "PETR4"
    quantidade: float = 100
    valor_investido: float = 2800.50
    tipo_id: int = 1

class InvestimentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID do investimento.
    """
    id: int = 1

class InvestimentoViewSchema(BaseModel):
    """ Define como um investimento será retornado.
    """
    id: int = 1
    nome_ativo: str = "PETR4"
    quantidade: float = 100
    valor_investido: float = 2800.50
    tipo: TipoInvestimentoViewSchema

class ListagemInvestimentosSchema(BaseModel):
    """ Define como uma listagem de investimentos será retornada.
    """
    investimentos:List[InvestimentoViewSchema]

def apresenta_investimentos(investimentos: List[Investimento]):
    """ Retorna uma representação do investimento seguindo o schema definido em
        ListagemInvestimentosSchema.
    """
    result = []
    for investimento in investimentos:
        result.append({
            "id": investimento.id,
            "nome_ativo": investimento.nome_ativo,
            "quantidade": investimento.quantidade,
            "valor_investido": investimento.valor_investido,
            "tipo": {
                "id": investimento.tipo.id,
                "nome": investimento.tipo.nome
            }
        })

    return {"investimentos": result}

class InvestimentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int

def apresenta_investimento(investimento: Investimento):
    """ Retorna uma representação do investimento seguindo o schema definido em
        InvestimentoViewSchema.
    """
    return {
        "id": investimento.id,
        "nome_ativo": investimento.nome_ativo,
        "quantidade": investimento.quantidade,
        "valor_investido": investimento.valor_investido,
        "tipo": {
            "id": investimento.tipo.id,
            "nome": investimento.tipo.nome
        }
    }
