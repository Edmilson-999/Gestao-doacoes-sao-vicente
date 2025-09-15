from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Beneficiario(Base):
    __tablename__ = 'beneficiarios'
    nif = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer)
    endereco = Column(String)
    contacto = Column(String)
    num_agregado = Column(Integer)
    necessidades = Column(String)
    observacoes = Column(String)

class Doacao(Base):
    __tablename__ = 'doacoes'
    id = Column(Integer, primary_key=True)
    instituicao = Column(String, nullable=False)
    beneficiario_nif = Column(String, ForeignKey('beneficiarios.nif'), nullable=False)
    tipo = Column(String)
    quantidade = Column(Integer)
    data = Column(Date)
    local = Column(String)
    preco_medio = Column(Float)

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    instituicao = Column(String, nullable=False)
    tipo = Column(String)
    quantidade_entrada = Column(Integer)
    origem = Column(String)
    quantidade_saida = Column(Integer)
    destino = Column(String)
    saldo = Column(Integer)