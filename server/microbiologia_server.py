from shiny import Inputs, Outputs, Session, module, render, reactive
from shinywidgets import render_widget
import plotly.express as px
from processamento import microbiologia_processamento
from processamento.filtros_processamento import *
import pandas as pd
import numpy as np
import datetime

@module.server
def microbiologia_server(input: Inputs, output: Outputs, session: Session, microrganismos_dict, motivo_admissao_dict, diagnosticos_dict):
    #Fetch da base de dados do DataFrame completo
    microbiologia_inicial = microbiologia_processamento.get_microbiologia_df()
    #Variável reativa inicializada com o DataFrame com todos os pacientes
    microbiologia_reactive = reactive.value(microbiologia_inicial)
    
    #Executada quando houver qualquer alteração em algum dos inputs
    #Copia o dataframe inicial com todos os pacientes e microrganismos, para depois aplicar os filtros
    #Coloca na variavel reativa o dataframe com os pacientes filtrado
    @reactive.effect
    def filtros():
        microbiologia_df = microbiologia_inicial.copy()

        #Filtro de idade
        microbiologia_df = filtro_idade(microbiologia_df, input.slider_age_microbiologia())
        #Filtro MFI 
        microbiologia_df = filtro_mfi(microbiologia_df, input.selectize_MFI_microbiologia())
        #Filtro SAPS
        microbiologia_df = filtro_saps(microbiologia_df, input.selectize_SAPS_microbiologia())
        #Filtro de hospitais
        microbiologia_df = filtro_hospitais(microbiologia_df, input.selectize_hospitais_microbiologia())
        #Filtro de motivo da admissão
        microbiologia_df = filtro_motivos_admissao(microbiologia_df, input.selectize_motivo_admissao_microbiologia(), motivo_admissao_dict)
        #Filtro de diagnóstico
        microbiologia_df = filtro_diagnostico(microbiologia_df, input.selectize_diagnostico_microbiologia(), diagnosticos_dict)
        #Filtro de microrganismos
        microbiologia_df = filtro_microrganismos(microbiologia_df, input.selectize_microrganismos_microbiologia(), microrganismos_dict)
        #Filtro de tipo de hospital
        microbiologia_df = filtro_tipo_hospital(microbiologia_df, input.selectize_tipo_hospital_microbiologia())
        #Filtro de região
        microbiologia_df = filtro_regiao(microbiologia_df, input.selectize_regiao_microbiologia())
        #Filtro de estado
        microbiologia_df = filtro_estado(microbiologia_df, input.selectize_estado_microbiologia())

        microbiologia_reactive.set(microbiologia_df)


    #Função auxiliar de frequencia_microrganismos, adiciona % ao final da string
    def add_perc(num):
        if (num != '0.0'):
            return num + '%'
        return '0.00%'

    #Constroi o DataFrame com os meses e a % por mês a partir das mudanças aplicadas pelos filtros
    #Retorna o DataFrame finalizado
    @reactive.calc
    def frequencia_microrganismos():
        microbiologia_df = microbiologia_reactive().copy()
        microbiologia_df.reset_index(drop=True, inplace=True)

        #Retira as colunas de filtro
        microbiologia_df = microbiologia_df[["infec_coleta_data", "pathogen_type_name"]]

        #Cria dataframes para cada período
        datas = [3, 6, 12, 36, 72]
        dataframes = []
        for nDias in range(len(datas)):
            meses = str(datas[nDias]) + ' meses'
            mesesPerc = '% ' + str(datas[nDias]) + ' meses'
            date_before = np.datetime64(datetime.date(2023, 12, 31) - datetime.timedelta(days=datas[nDias] * 30))
            dataframes.append(microbiologia_df[microbiologia_df['infec_coleta_data'] >= date_before])
            dataframes[nDias] = dataframes[nDias].rename(columns={'infec_coleta_data': meses, 'pathogen_type_name': 'Microrganismo'})
            dataframes[nDias] = dataframes[nDias].groupby("Microrganismo").count()
            dataframes[nDias][mesesPerc] = 100 * dataframes[nDias][meses] / dataframes[nDias][meses].sum()
            dataframes[nDias][mesesPerc] = dataframes[nDias][mesesPerc].round(2)

        #Cria um dataframe com todos os períodos unidos
        microrganismos_df = dataframes[0]
        for i in range(1, len(dataframes)):
            microrganismos_df = pd.merge(microrganismos_df, dataframes[i], how='outer', on='Microrganismo')

        #Adiciona a %
        microrganismos_df.reset_index(drop=False, inplace=True)
        microrganismos_df.fillna(0, inplace=True)
        for i in range(len(dataframes)):
            mesesPerc = '% ' + str(datas[i]) + ' meses'
            microrganismos_df[mesesPerc] = microrganismos_df[mesesPerc].astype(str).apply(add_perc)
        return microrganismos_df


    #DataFrame dos microrganismos
    #Chama a função reativa que cria a tabela final
    @render.data_frame
    def tabela_frequencia_microrganismo():
        return render.DataGrid(frequencia_microrganismos())


    #Download do DataFrame dos microrganismos
    #Chama a função reativa que cria a tabela final
    @render.download(filename=lambda: f"frequencia-micorganismo-{datetime.datetime.now()}.csv")
    async def download_tabela_frequencia_microrganismo():
        yield frequencia_microrganismos().to_csv(index=None, sep=';')


    #Função auxiliar da função frequencia_resistente_inicializa
    #Faz a conversão da data como Datetime para uma string
    #Formato: AAAA/MM - Esse formato garante que a tabela fique organizada crescentemente
    def data_to_string(valor):
        if (valor.month < 10):
            return str(valor.year) + '/' + '0' + str(valor.month)
        return str(valor.year) + '/' + str(valor.month)


    @reactive.calc
    def frequencia_resistentes():
        microbiologia = microbiologia_reactive().copy()
        microbiologia = microbiologia[["infec_coleta_data", "pathogen_type_name", "resistente"]]
        #Filtra pelas resistentes e não resistentes
        resistentes = microbiologia[microbiologia.resistente == 'Sim'].copy()
        sensiveis = microbiologia[microbiologia.resistente != 'Sim'].copy()
        resistentes['infec_coleta_data'] = resistentes['infec_coleta_data'].apply(data_to_string)
        sensiveis['infec_coleta_data'] = sensiveis['infec_coleta_data'].apply(data_to_string)
        resistentes = resistentes.groupby(["pathogen_type_name", "infec_coleta_data"]).count()
        with pd.option_context('future.no_silent_downcasting', True):
            sensiveis = sensiveis.fillna(0)
        sensiveis = sensiveis.groupby(["pathogen_type_name", "infec_coleta_data"]).count()
        sensiveis.rename(columns={"resistente": "sensiveis"}, inplace=True)
        resistentes = pd.concat([sensiveis, resistentes], sort=False)

        resistentes = resistentes.groupby(["infec_coleta_data"]).agg({'resistente': 'sum', 'sensiveis': 'sum'}).reset_index()
        return resistentes

    @render.data_frame
    def tabela_microrganismos_resistentes():
        return render.DataGrid(frequencia_resistentes())
    

    @render_widget
    def grafico_microrganismos_resistentes():
        resistentes_plot = px.bar(frequencia_resistentes(), x="infec_coleta_data", y=["resistente", "sensiveis"])
        return resistentes_plot  