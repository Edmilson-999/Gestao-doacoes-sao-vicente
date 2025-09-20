import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import String, Integer
from config import DATABASE_URI
from models import Beneficiario

# Configurar pandas para evitar FutureWarning
pd.set_option('future.no_silent_downcasting', True)

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Ler Excel, ajustando skiprows para pular cabeçalhos
    df = pd.read_excel('../data/Lista Pessoas.xlsx', sheet_name='Folha2', skiprows=3, header=None)
    
    # Verificar colunas esperadas
    expected_columns = ['n', 'nome', 'idade', 'menina_0_6', 'menina_6_10', 'menina_maior_10', 
                        'menino_0_6', 'menino_6_10', 'menino_maior_10', 'adultos', 
                        'total_agregado', 'zona_residencia', 'perdas', 'observacoes']
    if len(df.columns) < len(expected_columns):
        print(f"Aviso: O Excel tem {len(df.columns)} colunas, esperado {len(expected_columns)}. Ajustando...")
    df.columns = expected_columns[:len(df.columns)]
    
    # Log para depuração: mostrar tipos de dados
    print("Tipos de dados das colunas:")
    print(df.dtypes)
    
    # Limpar e preparar dados
    df = df.dropna(subset=['nome'])  # Ignorar linhas sem nome
    df = df[df['nome'] != 'NOME']   # Remover linhas de cabeçalho
    
    # Converter total_agregado para numérico
    if 'total_agregado' in df.columns:
        df['num_agregado'] = pd.to_numeric(df['total_agregado'], errors='coerce').fillna(0).astype(int)
    else:
        print("Coluna 'total_agregado' não encontrada. Usando 0 como padrão.")
        df['num_agregado'] = 0
    
    # Converter colunas para strings, tratando nulos
    df['perdas'] = df.get('perdas', '').astype(str).replace('nan', '')
    df['observacoes'] = df.get('observacoes', '').astype(str).replace('nan', '')
    df['necessidades'] = df['perdas'] + ', ' + df['observacoes']
    df['endereco'] = df.get('zona_residencia', '').astype(str).replace('nan', '')
    df['nif'] = 'NIF_' + df.index.astype(str)  # Placeholder para NIF --- df['nif'] = df['nif_coluna_do_excel']  # Nome da coluna com NIF
    df['contacto'] = ''
    
    # Log para depuração: mostrar primeiras linhas
    print("Primeiras 5 linhas do DataFrame após limpeza:")
    print(df[['nome', 'perdas', 'observacoes', 'necessidades']].head())
    
    # Inserir no banco usando to_sql
    df[['nif', 'nome', 'idade', 'endereco', 'contacto', 'num_agregado', 'necessidades', 'observacoes']].to_sql(
        'beneficiarios', 
        engine, 
        if_exists='append', 
        index=False,
        dtype={
            'nif': String,
            'nome': String,
            'idade': Integer,
            'endereco': String,
            'contacto': String,
            'num_agregado': Integer,
            'necessidades': String,
            'observacoes': String
        }
    )
    
    session.commit()
    print("Dados importados com sucesso!")

except Exception as e:
    print(f"Erro durante a importação: {e}")
    session.rollback()

finally:
    session.close()