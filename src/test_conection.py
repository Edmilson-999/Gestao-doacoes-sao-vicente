from sqlalchemy import create_engine
from config import DATABASE_URI

try:
    engine = create_engine(DATABASE_URI)
    with engine.connect() as connection:
        print("Conexão com o banco de dados 'gestao_doacoes' estabelecida com sucesso!")
except Exception as e:
       print(f"Erro ao conectar ao banco: {e}")