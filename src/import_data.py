import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Beneficiario

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_excel('../data/Lista Pessoas.xlsx', sheet_name='Folha2', skiprows=2, header=None)
df.columns = ['n', 'nome', 'idade', 'menina_0_6', 'menina_6_10', 'menina_maior_10', 'menino_0_6', 'menino_6_10', 'menino_maior_10', 'adultos', 'total_agregado', 'zona_residencia', 'perdas', 'observacoes']

df = df.dropna(subset=['nome'])
df['num_agregado'] = df['total_agregado'].fillna(0).astype(int)
df['necessidades'] = df['perdas'].fillna('') + ', ' + df['observacoes'].fillna('')
df['endereco'] = df['zona_residencia'].fillna('')
df['nif'] = 'NIF_' + df.index.astype(str)
df['contacto'] = ''

for index, row in df.iterrows():
    benef = Beneficiario(
        nif=row['nif'],
        nome=row['nome'],
        idade=row['idade'] if pd.notnull(row['idade']) else None,
        endereco=row['endereco'],
        contacto=row['contacto'],
        num_agregado=row['num_agregado'],
        necessidades=row['necessidades'],
        observacoes=row['observacoes']
    )
    session.add(benef)

session.commit()
session.close()
print("Dados importados com sucesso!")