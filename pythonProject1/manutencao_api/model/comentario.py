import string

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union
from model import Base


class Comentario(Base):
    """
        Representa um comentário dentro do sistema.

        Atributos:
            id (int): Identificador único para o comentário.
            texto (str): Texto do comentário.
            data_insercao (datetime): Data e hora em que o comentário foi inserido.
            equipamento (str): Chave estrangeira que referencia o `Equipamento` associado.

        Relacionamentos:
            Equipamento: Um `Comentario` está associado a um `Equipamento`.
    """

    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    equipamento = Column(String, ForeignKey("equipamento.pk_tag"), nullable=False)

    def __init__(self, texto:str, data_insercao:Union[datetime,None]=None):
        """
        Inicializa uma nova instância de Comentario.

        Args:
            texto (str): Texto do comentário.
            data_insercao (datetime, optional): Data e hora em que o comentário foi inserido.
                Se nenhum valor for fornecido, a data e hora atuais serão usadas.
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
