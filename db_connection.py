# db_connection.py

import configparser
from psycopg2 import OperationalError
import sqlalchemy

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
        print("Conexão bem-sucedida!")
        return connection
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None