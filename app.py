from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Investimento, TipoInvestimento
from schemas import *
from flask_cors import CORS

# Informações sobre a API
info = Info(title="Minha API - Controle de Investimentos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo as tags para organização no Swagger
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
investimento_tag = Tag(name="Investimento", description="Adição, visualização, edição e remoção de investimentos à carteira")
tipo_investimento_tag = Tag(name="Tipo de Investimento", description="Adição e listagem de tipos de investimentos (categorias)")


# Rota raiz que redireciona para a documentação
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota para adicionar um novo tipo de investimento (categoria)
@app.post('/tipo_investimento', tags=[tipo_investimento_tag],
          responses={"200": TipoInvestimentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tipo_investimento(body: TipoInvestimentoSchema):
    """Adiciona um novo Tipo de Investimento (categoria) à base de dados.

    Retorna uma representação do tipo de investimento criado.
    """
    tipo_investimento = TipoInvestimento(nome=body.nome)

    try:
        session = Session()
        session.add(tipo_investimento)
        session.commit()
        return {"id": tipo_investimento.id, "nome": tipo_investimento.nome}, 200
    except IntegrityError:
        error_msg = "Tipo de investimento com este nome já existe na base."
        return {"message": error_msg}, 409
    except Exception:
        error_msg = "Não foi possível salvar novo tipo de investimento."
        return {"message": error_msg}, 400

# Rota para listar todos os tipos de investimento
@app.get('/tipos_investimento', tags=[tipo_investimento_tag],
         responses={"200": ListagemTiposInvestimentoSchema, "404": ErrorSchema})
def get_tipos_investimento():
    """Faz a busca por todos os Tipos de Investimento cadastrados.

    Retorna uma representação da listagem de tipos de investimento.
    """
    session = Session()
    tipos = session.query(TipoInvestimento).all()

    if not tipos:
        return {"tipos_investimento": []}, 200
    else:
        return {"tipos_investimento": [{"id": t.id, "nome": t.nome} for t in tipos]}, 200


# Rota para adicionar um novo investimento à carteira
@app.post('/investimento', tags=[investimento_tag],
          responses={"200": InvestimentoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def add_investimento(body: InvestimentoSchema):
    """Adiciona um novo Investimento à carteira.

    Retorna uma representação do investimento adicionado.
    """
    session = Session()
    # Verifica se o tipo de investimento (categoria) existe
    tipo_investimento = session.query(TipoInvestimento).filter_by(id=body.tipo_id).first()
    if not tipo_investimento:
        error_msg = "Tipo de Investimento não encontrado."
        return {"message": error_msg}, 404

    investimento = Investimento(
        nome_ativo=body.nome_ativo,
        quantidade=body.quantidade,
        valor_investido=body.valor_investido,
        tipo_id=body.tipo_id
    )

    try:
        session.add(investimento)
        session.commit()
        return apresenta_investimento(investimento), 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo investimento."
        return {"message": error_msg, "details": str(e)}, 400


# Rota para listar todos os investimentos da carteira
@app.get('/investimentos', tags=[investimento_tag],
         responses={"200": ListagemInvestimentosSchema, "404": ErrorSchema})
def get_investimentos():
    """Faz a busca por todos os Investimentos cadastrados na carteira.

    Retorna uma representação da listagem de investimentos.
    """
    session = Session()
    investimentos = session.query(Investimento).all()

    if not investimentos:
        return {"investimentos": []}, 200
    else:
        return apresenta_investimentos(investimentos), 200


# Rota para buscar um investimento específico pelo ID
@app.get('/investimento', tags=[investimento_tag],
         responses={"200": InvestimentoViewSchema, "404": ErrorSchema})
def get_investimento(query: InvestimentoBuscaSchema):
    """Faz a busca por um Investimento a partir do ID.

    Retorna uma representação do investimento encontrado.
    """
    investimento_id = query.id
    session = Session()
    investimento = session.query(Investimento).filter(Investimento.id == investimento_id).first()

    if not investimento:
        error_msg = "Investimento não encontrado na base."
        return {"message": error_msg}, 404
    else:
        return apresenta_investimento(investimento), 200

# Rota para deletar um investimento pelo ID
@app.delete('/investimento', tags=[investimento_tag],
            responses={"200": InvestimentoDelSchema, "404": ErrorSchema})
def del_investimento(query: InvestimentoBuscaSchema):
    """Deleta um Investimento a partir do ID informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    investimento_id = query.id
    session = Session()
    count = session.query(Investimento).filter(Investimento.id == investimento_id).delete()
    session.commit()

    if count:
        return {"mesage": "Investimento removido", "id": investimento_id}
    else:
        error_msg = "Investimento não encontrado na base."
        return {"mesage": error_msg}, 404

# Rota para editar um investimento existente
@app.put('/investimento', tags=[investimento_tag],
         responses={"200": InvestimentoViewSchema, "404": ErrorSchema})
def update_investimento(query: InvestimentoBuscaSchema, body: InvestimentoSchema):
    """Edita um investimento existente na base de dados.
    """
    investimento_id = query.id
    session = Session()
    investimento = session.query(Investimento).filter(Investimento.id == investimento_id).first()

    if not investimento:
        error_msg = "Investimento não encontrado na base."
        return {"message": error_msg}, 404

    # Verifica se a nova categoria existe
    tipo_investimento = session.query(TipoInvestimento).filter_by(id=body.tipo_id).first()
    if not tipo_investimento:
        error_msg = "Tipo de Investimento não encontrado."
        return {"message": error_msg}, 404

    # Atualiza os dados
    investimento.nome_ativo = body.nome_ativo
    investimento.quantidade = body.quantidade
    investimento.valor_investido = body.valor_investido
    investimento.tipo_id = body.tipo_id
    session.commit()

    return apresenta_investimento(investimento), 200