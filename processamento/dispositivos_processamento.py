import pandas
import numpy as np
import datetime
import plotly.express as px
from db_connection import create_connection


def get_dispositivos_df():
    # Conectar ao banco de dados
    conn = create_connection()
    if not conn:
        return pandas.DataFrame()  # Retornar um DataFrame vazio em caso de falha na conexão
    try:
        # Executar as consultas SQL para obter os dados das tabelas Admissao e Microbiologia
        query = query = 'SELECT * FROM public.devices'
        dfdispositivos = pandas.read_sql_query(query, conn,index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"])
        dfdispositivos.reset_index(inplace=True)
        return dfdispositivos
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return pandas.DataFrame()  # Retornar um DataFrame vazio em caso de erro
    finally:
        conn.close()
