import pandas
import numpy as np
import datetime
import plotly.express as px
from db_connection import create_connection, fetch_from_db
from processamento.filtros_processamento import filtro_diagnostico, filtro_hospitais, filtro_idade, filtro_mfi, filtro_microrganismos, filtro_motivos_admissao, filtro_saps

def get_microrganismos_dict():
    viewmicrorganismos = fetch_from_db('SELECT * FROM public.vwmicrorganismos')
    return viewmicrorganismos.to_dict()['pathogen_type_name']

def get_microbiologia_df():
    viewFreqIdentMicro = fetch_from_db('SELECT * FROM public.vwfreqidentmicrorganismos', 
                                       index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"])
    return viewFreqIdentMicro


def get_hospitais_dict():
    hospitais = pandas.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Banco CCIH_HMV.csv", 
                                    sep=';', encoding='utf-8', low_memory=True, 
                                )
    hospitais = hospitais.rename(columns={ hospitais.columns[0]: "hospital_code" })

    hospitais = hospitais[['hospital_code', 'id_inst']]
    hospitais = hospitais.drop_duplicates(subset='hospital_code').set_index('hospital_code')

    return hospitais.to_dict()['id_inst']


def get_motivos_admissao_dict(motivo_admissao):
    motivo_admissao = motivo_admissao.reset_index()
    motivo_admissao = motivo_admissao[['admission_reason_name']]
    motivo_admissao = motivo_admissao.drop_duplicates()
    return motivo_admissao.to_dict()['admission_reason_name']


def get_diagnosticos_dict(diagnosticos):
    diagnosticos = diagnosticos.reset_index()
    diagnosticos = diagnosticos[['admission_main_diagnosis_name']]
    diagnosticos = diagnosticos.drop_duplicates()
    return diagnosticos.to_dict()['admission_main_diagnosis_name']

def get_amostra_dict():
    tipo_especime = {
        "Sangue": []

    }



def get_estados_dict():
    estados_brasil = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AM": "Amazonas",
        "AP": "Amapá",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MG": "Minas Gerais",
        "MS": "Mato Grosso do Sul",
        "MT": "Mato Grosso",
        "PA": "Pará",
        "PB": "Paraíba",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "PR": "Paraná",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RO": "Rondônia",
        "RR": "Roraima",
        "RS": "Rio Grande do Sul",
        "SC": "Santa Catarina",
        "SE": "Sergipe",
        "SP": "São Paulo",
        "TO": "Tocantins"
    }
    return estados_brasil