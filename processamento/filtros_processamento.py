import pandas as pd

#O dataframe recebido precisa ter a coluna saps3points
#Retorna as linhas da tabela cujo saps está entre o intervalo
#Como é possível selecionar mais de um intervalo, é verificado se o intervalo não foi selecionado
#Se o intervalo não foi selecionado, retira as linhas que estão neste intervalo
#Código dos SAPS selecionados, 0 = 0-34, 1 = 35-45, 2 = 55-74, 3 = 75-95, 4 = >95 
def filtro_saps(dataframe, saps_selecionados):
    if (len(saps_selecionados.get()) > 0):
        if ('0' not in saps_selecionados.get()):
            dataframe = dataframe[dataframe['saps3points'] >= 35]
        if ('1' not in saps_selecionados.get()):
            dataframe = dataframe[~((35 <= dataframe['saps3points']) & (dataframe['saps3points'] <= 54))]
        if ('2' not in saps_selecionados.get()):
            dataframe = dataframe[~((55 <= dataframe['saps3points']) & (dataframe['saps3points'] <= 74))]  
        if ('3' not in saps_selecionados.get()):
            dataframe = dataframe[~((75 <= dataframe['saps3points']) & (dataframe['saps3points'] <= 95))] 
        if ('4' not in saps_selecionados.get()):
            dataframe = dataframe[dataframe['saps3points'] < 95]
    return dataframe

#dataframe - O dataframe recebido precisa ter a coluna pathogen_type_name
#microrganismos_selecionados - Recebe os microrganismos selecionados
#microrganismos_dict - Precisa pegar o código daquele microrganismo de um dicionário de conversão que retorna o nome 
#do microrganismo como string
def filtro_microrganismos(dataframe, microrganismos_selecionados, microganismos_dict):
    #Se algum microrganismo foi selecionado
    if (len(microrganismos_selecionados.get()) > 0):
        #Lista das strings obtida a partir dos códigos no dicionário
        micro_filtrados = []
        for val in microrganismos_selecionados.get():
            #Converte o código inteiro na string com o nome do microrganismo e append esse nome na lista
            micro_filtrados.append(microganismos_dict[int(val)])
        #Verifica se o microrganismo do dataframe está na lista
        dataframe = dataframe[dataframe.pathogen_type_name.isin(micro_filtrados)]
    return dataframe

#dataframe - O dataframe recebido precisa ter a coluna mfi_points
#mfi_selecionados - Recebe os mfi selecionados, código NF (Non Frail), PF (Pre Frail) e F (Frail)
#Non Frail = 0, Pre Frail = 1 ou 2, Frail >=3
def filtro_mfi(dataframe, mfi_selecionados):
    if (len(mfi_selecionados.get()) > 0):
        if ('NF' not in mfi_selecionados.get()):
            dataframe = dataframe[dataframe['mfi_points'] != 0]
        if ('PF' not in mfi_selecionados.get()):
            dataframe = dataframe[~dataframe['mfi_points'].isin([1, 2])]
        if ('F' not in mfi_selecionados.get()):
            dataframe = dataframe[dataframe['mfi_points'] < 3] 
    return dataframe

#dataframe - O dataframe recebido precisa ter a coluna hospital_code
#hospitais_selecionados - Usa o código do hospital para verificar se está no DataFrame
def filtro_hospitais(dataframe, hospitais_selecionados):
    #Se algum hospital foi selecionado
    if (len(hospitais_selecionados.get()) > 0):
        #Verifica se o código do hospital está dentre os selecionados
        dataframe = dataframe.loc[dataframe['hospital_code'].isin(hospitais_selecionados.get())]
    return dataframe

#dataframe - Dataframe com a coluna age
#age_range - Tupla (IDADE_MIN, IDADE_MAX) no range procurado
def filtro_idade(dataframe, age_range):
    #Seleciona todas as linhas acima da IDADE_MIN
    dataframe = dataframe[dataframe['age'] >= age_range[0]]
    #Seleciona todas as linhas abaixo da IDADE_MAX
    dataframe = dataframe[dataframe['age'] <= age_range[1]]
    return dataframe

#dataframe - Dataframe com a coluna admission_reason_name
#motivos_selecionados - Usa um valor numérico como código do motivo
#motivos_dict - Faz a conversão do valor numérico do motivo à string
def filtro_motivos_admissao(dataframe, motivos_selecionados, motivos_dict):
    #Se algum motivo foi selecionado
    if (len(motivos_selecionados.get()) > 0):
            motivos_lista = []
            for val in motivos_selecionados.get():
                motivos_lista.append(motivos_dict[int(val)])
            dataframe = dataframe.loc[dataframe['admission_reason_name'].isin(motivos_lista)]
    return dataframe

#dataframe - Dataframe com a coluna admission_main_diagnosis_name
#diagnosticos_selecionados - Usa um valor numérico como código do diagnóstico
#diagnosticos_dict - Faz a conversão do valor numérico do motivo à string
def filtro_diagnostico(dataframe, diagnosticos_selecionados, diagnosticos_dict):
    #Se algum diagnostico foi selecionado
    if (len(diagnosticos_selecionados.get()) > 0):
        diagnosticos_lista = []
        for val in diagnosticos_selecionados.get():
            diagnosticos_lista.append(diagnosticos_dict[int(val)])
        dataframe = dataframe.loc[dataframe['admission_main_diagnosis_name'].isin(diagnosticos_lista)]
    return dataframe

#TODO
#dataframe - Dataframe com a coluna hospital_type_name
def filtro_tipo_hospital(dataframe, tipo_hospital_selecionado):
    #Se algum diagnostico foi selecionado
    #if (len(tipo_hospital_selecionado.get()) > 0):
            #diagnosticos_lista.append(diagnosticos_dict[int(val)])
        #dataframe = dataframe.loc[dataframe['admission_main_diagnosis_name'].isin(diagnosticos_lista)]
    return dataframe