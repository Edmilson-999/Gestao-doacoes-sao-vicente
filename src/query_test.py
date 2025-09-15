from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Beneficiario

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
benefs = session.query(Beneficiario).all()
for b in benefs:
    print(f"NIF: {b.nif}, Nome: {b.nome}, Necessidades: {b.necessidades}")
session.close()