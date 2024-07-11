from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """
    Schema para representar uma mensagem de erro dentro da aplicação.

    Esta classe é utilizada para padronizar a forma como as mensagens de erro são enviadas
    aos usuários da API, garantindo que todas as mensagens de erro sigam um formato consistente.

    Attributes:
        message (str): A mensagem de erro que explica o que deu errado.
    """
    message: str
