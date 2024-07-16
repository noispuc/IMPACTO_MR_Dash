import pandas
import numpy as np
import datetime

def get_microrganismos_dict():
    microbiologia = pandas.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Microbiologia.csv", 
                                        sep=';', encoding='latin-1', low_memory=True, 
                                        usecols=["pathogen_type_name"])
    microbiologia.drop_duplicates(inplace=True)
    microbiologia.rename(columns={'pathogen_type_name': 'Microrganismos',}, inplace=True)
    microbiologia.sort_values(by='Microrganismos', inplace=True)
    return microbiologia.to_dict()


def add_perc(num):
    if (num != '0.0'):
        return num + '%'
    return '0.00%'


def get_microbiologia_df(admissao):
    #Abre o csv de Microbiologia
    microbiologia = pandas.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Microbiologia.csv", 
                                    sep=';', encoding='latin-1', low_memory=True, 
                                    index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"],
                                    usecols=["id_paciente", "id_hosp_internacao", "id_uti_internacao",
                                              "infec_coleta_data", "pathogen_type_name"], parse_dates=["infec_coleta_data"])
    admissao = admissao[["age", "hospital_code", "admission_reason_name"]]
    return microbiologia.join(admissao)

def frequencia_ident_isolados(microbiologia, age_range, hospitais_selecionados):
    microbiologia = microbiologia.copy()
    microbiologia.reset_index(drop=True, inplace=True)

    #Filtro de idade
    microbiologia = microbiologia[microbiologia['age'] >= age_range[0]]
    microbiologia = microbiologia[microbiologia['age'] <= age_range[1]]

    #Filtro de hospitais
    if (len(hospitais_selecionados.get()) > 0):
        microbiologia = microbiologia.loc[microbiologia['hospital_code'].isin(hospitais_selecionados.get())]


    microbiologia.drop(columns=['age', 'hospital_code', 'admission_reason_name'], inplace=True)
    datas = [3, 6, 12, 36, 72]
    dataframes = []
    for nDias in range(len(datas)):
        meses = str(datas[nDias]) + ' meses'
        mesesPerc = '% ' + str(datas[nDias]) + ' meses'
        date_before = np.datetime64(datetime.date(2023, 12, 31) - datetime.timedelta(days=datas[nDias] * 30))
        dataframes.append(microbiologia[microbiologia['infec_coleta_data'] >= date_before])
        dataframes[nDias] = dataframes[nDias].rename(columns={'infec_coleta_data': meses, 'pathogen_type_name': 'Microrganismo'})
        dataframes[nDias] = dataframes[nDias].groupby("Microrganismo").count()
        dataframes[nDias][mesesPerc] = 100 * dataframes[nDias][meses] / dataframes[nDias][meses].sum()
        dataframes[nDias][mesesPerc] = dataframes[nDias][mesesPerc].round(2)

    #Cria um dataframe com todos os períodos unidos
    resultado = dataframes[0]
    for i in range(1, len(dataframes)):
        resultado = pandas.merge(resultado, dataframes[i], how='outer', on='Microrganismo')

    resultado.reset_index(drop=False, inplace=True)
    resultado.fillna(0, inplace=True)
    for i in range(len(dataframes)):
        mesesPerc = '% ' + str(datas[i]) + ' meses'
        resultado[mesesPerc] = resultado[mesesPerc].astype(str).apply(add_perc)
    
    return resultado

def data(valor):
    if (valor.month < 10):
        return str(valor.year) + '/' + '0' + str(valor.month)
    return str(valor.year) + '/' + str(valor.month)

def isolamento_bacterias_resistentes():
    microbiologia = pandas.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Microbiologia.csv", 
                                    sep=';', encoding='latin-1', low_memory=True, 
                                    usecols=["infec_coleta_data", "pathogen_type_name", "resistente"], parse_dates=["infec_coleta_data"])
    
    #Filtra somente pelas resistentes
    resistentes = microbiologia[microbiologia.resistente == 'Sim']
    resistentes['infec_coleta_data'] = resistentes['infec_coleta_data'].apply(data)
    resistentes = resistentes.groupby(["pathogen_type_name", "infec_coleta_data"]).count()
    resistentes.reset_index(drop=False, inplace=True)
    return resistentes


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