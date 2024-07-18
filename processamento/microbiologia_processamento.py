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
    return microbiologia.to_dict()['Microrganismos']


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
    admissao = admissao[["age", "hospital_code", "admission_reason_name", "mfi_points", "saps3points", "admission_main_diagnosis_name"]]
    return microbiologia.join(admissao)


def frequencia_ident_isolados(microbiologia, age_range, hospitais_selecionados, motivos_selecionados, motivos_dict, microrganismos_selecionados, microganismos_dict, mfi_selecionados, saps_selecionados, diagnosticos_selecionados, diagnosticos_dict):
    microbiologia = microbiologia.copy()
    microbiologia.reset_index(drop=True, inplace=True)

    #Filtro de idade
    microbiologia = microbiologia[microbiologia['age'] >= age_range[0]]
    microbiologia = microbiologia[microbiologia['age'] <= age_range[1]]

    #Filtro MFI
    if (len(mfi_selecionados.get()) > 0):
        if ('NF' not in mfi_selecionados.get()):
            microbiologia = microbiologia[microbiologia['mfi_points'] != 0]
        if ('PF' not in mfi_selecionados.get()):
            microbiologia = microbiologia[~microbiologia['mfi_points'].isin([1, 2])]
        if ('F' not in mfi_selecionados.get()):
            microbiologia = microbiologia[microbiologia['mfi_points'] < 3]    

    #Filtro SAPS
    if (len(saps_selecionados.get()) > 0):
        if ('0' not in saps_selecionados.get()):
            microbiologia = microbiologia[microbiologia['saps3points'] >= 35]
        if ('1' not in saps_selecionados.get()):
            microbiologia = microbiologia[~((35 <= microbiologia['saps3points']) & (microbiologia['saps3points'] <= 54))]
        if ('2' not in saps_selecionados.get()):
            microbiologia = microbiologia[~((55 <= microbiologia['saps3points']) & (microbiologia['saps3points'] <= 74))]  
        if ('3' not in saps_selecionados.get()):
            microbiologia = microbiologia[~((75 <= microbiologia['saps3points']) & (microbiologia['saps3points'] <= 95))] 
        if ('4' not in saps_selecionados.get()):
            microbiologia = microbiologia[microbiologia['saps3points'] < 95]


    #Filtro de hospitais
    if (len(hospitais_selecionados.get()) > 0):
        microbiologia = microbiologia.loc[microbiologia['hospital_code'].isin(hospitais_selecionados.get())]


    #Filtro de motivo da admissão
    if (len(motivos_selecionados.get()) > 0):
        motivos_lista = []
        for val in motivos_selecionados.get():
            motivos_lista.append(motivos_dict[int(val)])
        microbiologia = microbiologia.loc[microbiologia['admission_reason_name'].isin(motivos_lista)]

    #Filtro de diagnóstico
    if (len(diagnosticos_selecionados.get()) > 0):
        diagnosticos_lista = []
        for val in diagnosticos_selecionados.get():
            diagnosticos_lista.append(diagnosticos_dict[int(val)])
        microbiologia = microbiologia.loc[microbiologia['admission_main_diagnosis_name'].isin(diagnosticos_lista)]

    #Retira as colunas de filtro
    microbiologia.drop(columns=['age', 'hospital_code', 'admission_reason_name', 'mfi_points', 'saps3points', 'admission_main_diagnosis_name'], inplace=True)


    #Cria dataframes para cada período
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

    #Adiciona a %
    resultado.reset_index(drop=False, inplace=True)
    resultado.fillna(0, inplace=True)
    for i in range(len(dataframes)):
        mesesPerc = '% ' + str(datas[i]) + ' meses'
        resultado[mesesPerc] = resultado[mesesPerc].astype(str).apply(add_perc)

    #Filtro de microrganismos
    if (len(microrganismos_selecionados.get()) > 0):
        micro_filtrados = []
        for val in microrganismos_selecionados.get():
            micro_filtrados.append(microganismos_dict[int(val)])
        resultado = resultado[resultado.Microrganismo.isin(micro_filtrados)]
    return resultado
    

def data(valor):
    if (valor.month < 10):
        return str(valor.year) + '/' + '0' + str(valor.month)
    return str(valor.year) + '/' + str(valor.month)


def frequencia_microrganismos_resistentes():
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


def get_diagnosticos_dict(diagnosticos):
    diagnosticos = diagnosticos.reset_index()
    diagnosticos = diagnosticos[['admission_main_diagnosis_name']]
    diagnosticos = diagnosticos.drop_duplicates()
    return diagnosticos.to_dict()['admission_main_diagnosis_name']