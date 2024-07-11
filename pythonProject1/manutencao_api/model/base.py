"""
Este módulo define a base declarativa para todos os modelos do SQLAlchemy.

A `Base` criada aqui é utilizada para derivar todos os modelos de banco de dados, permitindo que
o SQLAlchemy gerencie internamente os detalhes do mapeamento entre as classes Python e as tabelas
do banco de dados.
"""

from sqlalchemy.ext.declarative import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()
