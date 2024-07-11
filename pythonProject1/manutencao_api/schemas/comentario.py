from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """
        Schema para representar um novo comentário associado a um equipamento.

        Attributes:
            equipamento_id (int): Identificador do equipamento ao qual o comentário está associado.
            texto (str): Conteúdo textual do comentário.

        Note:
            Os valores padrão fornecidos aqui são apenas para exemplos. Em produção,
            normalmente não se incluiriam valores padrão para campos como `equipamento_id` e `texto`,
            a menos que haja uma razão específica para tal padrão.
    """
    equipamento_id: int = 1
    texto: str = "Manter os equipamentos em dia com a manutenção é o desejável!"
