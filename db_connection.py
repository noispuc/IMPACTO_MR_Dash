# db_connection.py

import configparser
import psycopg2
from psycopg2 import OperationalError

def create_connection():
    config = configparser.ConfigParser()
    config.read('db_open.ini')

    try:
        # Informações de conexão
        connection = psycopg2.connect(
            host=config['postgresql']['host'],
            port=config['postgresql']['port'],
            dbname=config['postgresql']['dbname'],
            user=config['postgresql']['user'],
            password=config['postgresql']['password']
        )
        print("Conexão bem-sucedida!")
        return connection
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Exemplo de uso
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.close()
