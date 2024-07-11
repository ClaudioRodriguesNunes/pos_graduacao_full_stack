from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from model import Base, Comentario


class Equipamento(Base):
    __tablename__ = 'equipamento'
    """
    Representa um equipamento dentro do sistema.

    Attributes:
        pk_tag (str): Identificador único do equipamento, usado como chave primária.
        nome (str): Nome do equipamento, como válvula, permutadores, vaso separador, etc.
        periodo (int): Periodo em meses do ciclo para a preventiva.
        data_instalacao (datetime): Data da instalação do equipamento.
        comentarios (list[Comentario]): Lista de comentários associados ao equipamento.
    """


    pk_tag = Column("pk_tag",String(10), primary_key=True)
    nome = Column(String(140))
    periodo = Column(Integer)
    data_instalacao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o tag e o comentário.
    # Essa relação é implicita, não está salva na tabela 'equipamento',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, pk_tag: str, nome: str, periodo: int,
                 data_instalacao:Union[DateTime,None] = None):
        """
        Inicializa uma nova instância da classe Equipamento.

        Args:
            pk_tag (str): TAG do equipamento.
            nome (str): Nome do equipamento.
            periodo (int): Número de meses até a próxima manutenção preventiva.
            data_instalacao (datetime, optional): Data de instalação do equipamento. Se não fornecido, usa a data atual.
        """
        self.pk_tag = pk_tag
        self.nome = nome
        self.periodo = periodo
        if data_instalacao:
            self.data_instalacao = data_instalacao

    def adiciona_comentario(self, comentario:Comentario):
        """
                Adiciona um novo comentário ao equipamento.

                Args:
                    comentario (Comentario): Objeto Comentario que será adicionado à lista de comentários do equipamento.
                """
        self.comentarios.append(comentario)
