
import pandas as pd

def get_desfecho_adm():

    admissoes = pd.read_csv("d:/MDR\MDR_Impacto_MR/analysis_impacto_R/data/Admissao.csv", 
                            sep=";", index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"], encoding='latin-1',)
    desfecho = pd.read_csv("d:/MDR/MDR_Impacto_MR/analysis_impacto_R/data\Desfecho.csv", 
                        sep=";", index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"], encoding='latin-1',)
    desfecho_adm = pd.merge(admissoes, desfecho, left_on=['id_paciente', 'id_hosp_internacao', 'id_uti_internacao'], right_on=['id_paciente', 'id_hosp_internacao', 'id_uti_internacao'], how='left')

    desfecho_adm['mes_ano_uti'] = pd.to_datetime(desfecho_adm['unit_admission_date'], errors='coerce')
    desfecho_adm['ano_uti'] = desfecho_adm['mes_ano_uti'].dt.year.astype(str)

    desfecho_adm = desfecho_adm.reset_index().drop_duplicates(subset='id_paciente', keep='first').set_index(['id_paciente', 'id_hosp_internacao', 'id_uti_internacao'])

    return desfecho_adm

def get_microbio():

    microbio = pd.read_csv("d:/MDR/MDR_Impacto_MR/analysis_impacto_R/data\Microbiologia.csv", 
                       sep=";", index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"], encoding='latin-1',)
    microbio['mes_ano_coleta'] = pd.to_datetime(microbio['infec_coleta_data'], errors='coerce')
    microbio['ano_coleta'] = microbio['mes_ano_coleta'].dt.year.astype(str)

    microbio = microbio.reset_index().drop_duplicates(subset='id_paciente', keep='first').set_index(['id_paciente', 'id_hosp_internacao', 'id_uti_internacao'])

    return microbio

def get_df_pacientes_dia(desfecho_adm, microbio):
    df_totalPositivos = microbio.merge(desfecho_adm, on=['id_paciente', 'id_hosp_internacao', 'id_uti_internacao'], how='left')\
                        .groupby(['hospital_code', 'ano_coleta'])\
                        .size()\
                        .reset_index(name='count')

    df_pacientes_dia = (
        desfecho_adm[['hospital_code', 'hospital_length_stay', 'unit_length_stay', 'ano_uti']]
        .groupby(['hospital_code', 'ano_uti'])
        .agg(total_hosp_length=('hospital_length_stay', 'sum'),
            total_unit_length=('unit_length_stay', 'sum'))
        .reset_index()
        .merge(df_totalPositivos, left_on=['hospital_code', 'ano_uti'], right_on=['hospital_code', 'ano_coleta'], how='left') \
                            .assign(positivos_hosp=lambda x: round(x['count'] * 1000 / x['total_hosp_length'], 1),
                                    positivos_uti=lambda x: round(x['count'] * 1000 / x['total_unit_length'], 1)) \
                            .drop(columns=['ano_coleta']) \
                            .set_index(['hospital_code', 'ano_uti'])
    )

    return df_pacientes_dia

def get_desfecho_juntas(desfecho_adm, microbio):
    coluna_desfecho = desfecho_adm \
                   .assign(obito=lambda x: (x['hospital_discharge_code'] == 'Óbito').astype(int)) \
                   .groupby(['hospital_code', 'ano_uti']).agg({'obito': ['sum', 'size']}) \
                   .reset_index() \
                   .assign(total_obito=lambda x: round(x['obito']['sum'] / x['obito']['size'], 1))

    coluna_desfecho_positivos = microbio.merge(desfecho_adm, on=['id_paciente', 'id_hosp_internacao', 'id_uti_internacao'], how='left') \
                                .assign(obito=lambda x: (x['hospital_discharge_code'] == 'Óbito').astype(int)) \
                                .groupby(['hospital_code', 'ano_uti']).agg({'obito': ['sum', 'size']}) \
                                .assign(positivos_obito=lambda x: round(x['obito']['sum'] / x['obito']['size'], 1))\
                                .reset_index()                            


    desfecho_juntas = coluna_desfecho.merge(coluna_desfecho_positivos, on=['hospital_code', 'ano_uti'], how='left')\
                        .drop(columns = [('obito_x',  'sum'),('obito_x', 'size'),
                                        ('obito_y',  'sum'),('obito_y', 'size')]) 
    desfecho_juntas.columns = ["".join(tup) for tup in desfecho_juntas.columns.to_flat_index()]

    return desfecho_juntas 

def get_tabela_indicadores(df_pacientes_dia, desfecho_juntas):
    tabela_indicadores = desfecho_juntas.merge(df_pacientes_dia,
                                        on=['hospital_code', 'ano_uti'], 
                                        how='left')\
                                    .rename(columns={"ano_uti_": "ano", 
                                                    "count": "quantidade_positivos",
                                                    'positivos_hosp': 'pacientes_dia_hosp',
                                                    'positivos_uti': 'pacientes_dia_uti'})

    return tabela_indicadores                 
