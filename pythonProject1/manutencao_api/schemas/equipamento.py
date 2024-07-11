from pydantic import BaseModel
from typing import Optional, List
from model.equipamento import Equipamento
from schemas import ComentarioSchema


class EquipamentoSchema(BaseModel):
    """
    Define o schema para um novo equipamento a ser inserido.
    """
    pk_tag: str = "V-33002-A"
    nome: str = "Vaso separador A"
    periodo: int = 12

class EquipamentoBuscaSchema(BaseModel):
    """
    Define o schema para a busca de equipamentos por TAG.
    """
    pk_tag: str


class ListagemEquipamentosSchema(BaseModel):
    """
    Define o schema para a listagem de equipamentos.
    """
    equipamentos:List[EquipamentoSchema]


def apresenta_Equipamentos(equipamentos: List[Equipamento]) -> object:
    """
    Retorna uma lista de equipamentos formatada conforme o EquipamentoSchema.

    Args:
        equipamentos (List[Equipamento]): Lista de instâncias de Equipamento.

    Returns:
        dict: Dicionário contendo a listagem de equipamentos.
    """
    result = []
    for equipamento in equipamentos:
        result.append({
            "tag": equipamento.pk_tag,
            "nome": equipamento.nome,
            "periodo": equipamento.periodo,
        })
    return {"equipamentos": result}


class EquipamentoViewSchema(BaseModel):
    """
    Define o schema para a visualização detalhada de um equipamento, incluindo comentários.
    """
    pk_tag: str
    nome: str
    periodo: int = 12
    total_cometarios: int = 1
    comentarios: List[ComentarioSchema]


class EquipamentoDelSchema(BaseModel):
    """
    Define o schema para o retorno após uma operação de deleção de equipamento.
    """
    message: str
    nome: str


def apresenta_Equipamento(equipamento: Equipamento):
    """
        Retorna uma representação detalhada de um único equipamento conforme EquipamentoViewSchema.

        Args:
            equipamento (Equipamento): A instância de Equipamento a ser representada.

        Returns:
            dict: Dicionário representando o equipamento detalhado.
    """
    return {
        "tag": equipamento.pk_tag,
        "nome": equipamento.nome,
        "periodo": equipamento.periodo,
        "total_cometarios": len(equipamento.comentarios),
        "comentarios": [{"texto": c.texto} for c in equipamento.comentarios]
    }
