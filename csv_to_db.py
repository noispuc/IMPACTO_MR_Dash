import pandas as pd
import sqlalchemy
import configparser
from psycopg2 import OperationalError

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

    # Create the engine to connect to the PostgreSQL database
    
    # Read data from CSV and load into a dataframe object
    admissao = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Admissao.csv", 
                        sep=';', encoding='latin-1', low_memory=True, 
                        parse_dates=["unit_admission_date", "hospital_admission_date"])
    
    antimicrobiano = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Antimicrobiano.csv", 
                        sep=';', encoding='latin-1', low_memory=True, 
                        parse_dates=["antimicrobial_begin_date", "antimicrobial_end_date"])

    banco = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Banco CCIH_HMV.csv", 
                        sep=';', encoding='utf-8', low_memory=True 
                        )

    desfecho = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Desfecho.csv", 
                        sep=';', encoding='latin-1', low_memory=True, 
                        parse_dates=["unit_discharge_date", "hospital_discharge_date"])

    microbiologia = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Microbiologia.csv", 
                        sep=';', encoding='latin-1', low_memory=True, 
                        parse_dates=["infec_coleta_data"])
    
    devices = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Devices.csv", 
                        sep=';', encoding='latin-1', low_memory=True, 
                        parse_dates=["placement_date", "removal_date"])

    fatores = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Fatores de risco institucionais.csv", 
                        sep=',', encoding='latin-1', low_memory=True
                        )

    fisiolab = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/FisioLab.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["unit_admission_date"], decimal=',')

    infeccao = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/infeccao.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["placement_date", "removal_date"])

    iras_ics = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/IRAS_ICS_confirmado.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["infection_date", "placement_date", 
                                     "removal_date", "infec_coleta_data_1",
                                     "infec_coleta_data_2", "infec_coleta_data_3"])

    iras_itu = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/IRAS_ITU_confirmado.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["infection_date", "placement_date",
                                     "removal_date", "infec_coleta_data_1",
                                     "infec_coleta_data_2"])

    iras_pav = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/IRAS_PAV_confirmado.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["infection_date", "placement_date",
                                     "removal_date", "infec_coleta_data_1", "infec_coleta_data_2",
                                     "infec_coleta_data_3", "infec_coleta_data_4"])
    
    qualidade_vida = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Qualidade_vida.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["dt_qol", "dt_qol_3m"])

    sintomas = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/Sintomas.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["infection_date"])

    sofa = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/SOFA.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["unit_admission_date"])

    swab = pd.read_csv("D:/MDR/MDR_Impacto_MR/data/SWAB.csv", 
                        sep=';', encoding='latin-1', low_memory=True,
                        parse_dates=["hospital_admission_date", "unit_admission_date",
                                     "unit_discharge_date", "hospital_discharge_date",
                                     "DataColeta"])
    print("Leitura concluida")
    
    # Write data into the table in PostgreSQL database
    admissao.to_sql(name='admissao', con=engine, if_exists='replace')
    antimicrobiano.to_sql(name='antimicrobiano', con=engine, if_exists='replace')
    microbiologia.to_sql(name='microbiologia', con=engine, if_exists='replace')
    banco.to_sql(name='banco', con=engine, if_exists='replace')
    desfecho.to_sql(name='desfecho', con=engine, if_exists='replace')
    devices.to_sql(name='devices', con=engine, if_exists='replace')
    fatores.to_sql(name='fatores', con=engine, if_exists='replace')
    fisiolab.to_sql(name='fisiolab', con=engine, if_exists='replace')
    infeccao.to_sql(name='infeccao', con=engine, if_exists='replace')
    iras_ics.to_sql(name='iras_ics', con=engine, if_exists='replace')
    iras_itu.to_sql(name='iras_itu', con=engine, if_exists='replace')
    iras_pav.to_sql(name='iras_pav', con=engine, if_exists='replace')
    qualidade_vida.to_sql(name='qualidade_vida', con=engine, if_exists='replace')
    sintomas.to_sql(name='sintomas', con=engine, if_exists='replace')
    sofa.to_sql(name='sofa', con=engine, if_exists='replace')
    swab.to_sql(name='swab', con=engine, if_exists='replace')
    print("Finalizado!")
    connection.close()
except OperationalError as e:
    print(f"Erro ao conectar ao banco de dados: {e}")