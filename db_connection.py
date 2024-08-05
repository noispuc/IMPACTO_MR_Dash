# db_connection.py

import configparser
from psycopg2 import OperationalError
import sqlalchemy
import pandas as pd

def create_connection():
    config = configparser.ConfigParser()
    config.read('db_open.ini')

    try:
        # Informações de conexão
        engine = sqlalchemy.create_engine('postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
                user=config['postgresql']['user'], 
                passwd=config['postgresql']['password'], 
                host=config['postgresql']['host'], 
                port=config['postgresql']['port'], 
                db=config['postgresql']['dbname']))
        
        connection = engine.connect()
        return connection
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    

def fetch_from_db(query, index_col=None):
    # Conectar ao banco de dados
    conn = create_connection()
    if not conn:
        return pd.DataFrame()  # Retornar um DataFrame vazio em caso de falha na conexão
    try:
        # Executar as consultas SQL para obter os dados das tabelas Admissao e Microbiologia
        dataframe = pd.read_sql_query(query, conn, index_col=index_col)
        return dataframe
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return pd.DataFrame()  # Retornar um DataFrame vazio em caso de erro
    finally:
        conn.close()