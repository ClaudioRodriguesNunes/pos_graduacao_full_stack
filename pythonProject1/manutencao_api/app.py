from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Equipamento, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="2.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
equipamento_tag = Tag(name="Equipamento", description="Adição, visualização e remoção de equipamentos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um equipamento cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para a escolha do estilo de documentação."""

    return redirect('/openapi')

@app.post('/equipamento', tags=[equipamento_tag],
          responses={"200": EquipamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_equipamento(form: EquipamentoSchema):
    """Adiciona um novo equipamento à base de dados e retorna uma representação deste equipamento."""

    equipamento = Equipamento(
        pk_tag=form.pk_tag,
        nome=form.nome,
        periodo=form.periodo)
    logger.debug(f"Adicionando equipamento de tag: '{equipamento.pk_tag}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando equipamento
        session.add(equipamento)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado equipamento de tag: '{equipamento.pk_tag}'")
        return apresenta_Equipamento(equipamento), 200

    except IntegrityError as e:
        # como a duplicidade do tag é a provável razão do IntegrityError
        error_msg = "Equipamento de mesmo tag já salvo na base :/"
        logger.warning(f"Erro ao adicionar tag '{equipamento.pk_tag}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar equipamento '{equipamento.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/equipamentos', tags=[equipamento_tag],
         responses={"200": ListagemEquipamentosSchema, "404": ErrorSchema})
def get_equipamentos():
    """Busca todos os equipamentos cadastrados e retorna uma listagem."""

    logger.debug(f"Coletando equipamentos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    equipamentos = session.query(Equipamento).all()

    if not equipamentos:
        # se não há equipamentos cadastrados
        return {"equipamentos": []}, 200
    else:
        logger.debug(f"%d equipamentos econtrados" % len(equipamentos))
        # retorna a representação de equipamento
        print(equipamentos)
        return apresenta_Equipamentos(equipamentos), 200


@app.get('/equipamento', tags=[equipamento_tag],
         responses={"200": EquipamentoViewSchema, "404": ErrorSchema})
def get_equipamento(query: EquipamentoBuscaSchema):
    """Busca um equipamento por TAG e retorna detalhes sobre o equipamento."""

    equipamento_id = query.id
    logger.debug(f"Coletando dados sobre equipamento #{equipamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    equipamento = session.query(Equipamento).filter(Equipamento.pk_tag == equipamento_id).first()

    if not equipamento:
        # se o equipamento não foi encontrado
        error_msg = "Equipamento não encontrado na base :/"
        logger.warning(f"Erro ao buscar equipamento '{equipamento_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Equipamento econtrado: '{equipamento.nome}'")
        # retorna a representação de equipamento
        return apresenta_Equipamento(equipamento), 200


@app.delete('/equipamento', tags=[equipamento_tag],
            responses={"200": EquipamentoDelSchema, "404": ErrorSchema})
def del_equipamento(query: EquipamentoBuscaSchema):
    """Deleta um equipamento com base no TAG fornecido e retorna uma mensagem de confirmação."""

    equipamento_nome = unquote(query.pk_tag)
    print(equipamento_nome)
    logger.debug(f"Deletando dados sobre equipamento #{equipamento_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Equipamento).filter(Equipamento.pk_tag == equipamento_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado equipamento #{equipamento_nome}")
        return {"mesage": "Equipamento removido", "id": equipamento_nome}
    else:
        # se o equipamento não foi encontrado
        error_msg = "Equipamento não encontrado na base :/"
        logger.warning(f"Erro ao deletar equipamento #'{equipamento_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": EquipamentoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona um novo comentário a um equipamento e retorna a representação atualizada do equipamento."""

    equipamento_id = form.equipamento_id
    logger.debug(f"Adicionando comentários ao equipamento #{equipamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo equipamento
    equipamento = session.query(Equipamento).filter(Equipamento.pk_tag == equipamento_id).first()

    if not equipamento:
        # se equipamento não encontrado
        error_msg = "Equipamento não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao equipamento '{equipamento_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao equipamento
    equipamento.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao equipamento #{equipamento_id}")

    # retorna a representação de equipamento
    return apresenta_Equipamento(equipamento), 200
