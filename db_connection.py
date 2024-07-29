# db_connection.py

import configparser
from psycopg2 import OperationalError
import sqlalchemy

def create_connection():
    config = configparser.ConfigParser()
    config.read('db_open.ini')

    try:
        # Informações de conexão
        engine = sqlalchemy.create_engine('postgresql://' +
                                          config['postgresql']['user'] + ':' +
                                          config['postgresql']['password'] + '@' +
                                          config['postgresql']['host'] + ':' + 
                                          config['postgresql']['port'] + '/' +
                                          config['postgresql']['dbname'])

        connection = engine.connect()
        print("Conexão bem-sucedida!")
        return connection
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Exemplo de uso
'''
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.close()
'''