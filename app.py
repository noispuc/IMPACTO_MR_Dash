from server import microbiologia_server, hospitais_server, dispositivos_server
from ui import microbiologia_ui, hospitais_ui, dispositivos_ui
from processamento import microbiologia_processamento, hospitais_processamento, dispositivos_processamento
from shiny import App, Inputs, ui, Outputs, Session
import pandas as pd

admissao = pd.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Admissao.csv", 
                        index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"],
                        sep=';', encoding='latin-1', low_memory=True, 
                        parse_dates=["unit_admission_date"])
desfecho = pd.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Desfecho.csv", 
                        sep=";", 
                        index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"], 
                        encoding='latin-1',)
microbiologia = pd.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Microbiologia.csv", 
                        sep=';', encoding='latin-1', low_memory=True, 
                        index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"], 
                        parse_dates=["infec_coleta_data"])

'''Microbiologia'''
microbiologia_df = microbiologia_processamento.get_microbiologia_df(admissao)
resistente_df = microbiologia_processamento.frequencia_resistente_inicializa(microbiologia)


'''Microbiologia - Filtros'''
microganismos_dict = microbiologia_processamento.get_microrganismos_dict()
hospitais_dict = microbiologia_processamento.get_hospitais_dict()
motivo_admissao_dict = microbiologia_processamento.get_motivos_admissao_dict(admissao[['admission_reason_name']])
diagnostico_dict = microbiologia_processamento.get_diagnosticos_dict(admissao[['admission_main_diagnosis_name']])

'''Hospitais'''
indicadores_df = hospitais_processamento.get_tabela_indicadores(admissao, microbiologia, desfecho)
'''dispositivos'''
dispositivos_df = dispositivos_processamento.get_dispositivos_df()

''' UI '''
app_ui = ui.page_navbar(  
        ui.nav_panel("Microbiologia", microbiologia_ui.microbiologia_ui("microbiologia", microganismos_dict, hospitais_dict, motivo_admissao_dict, diagnostico_dict)),
        ui.nav_panel("Antibióticos", "Placeholder"),  
        ui.nav_panel("Hospitais", hospitais_ui.hospitais_ui('hospitais')),  
        ui.nav_panel("Dispositivos", dispositivos_ui.dispositivos_ui('dispositivos')),  
        title="Impacto MR",  
        id="page",  
    )  

''' SERVER '''
def server(input: Inputs, output: Outputs, session: Session):
    microbiologia_server.microbiologia_server("microbiologia", microbiologia_df, resistente_df, microganismos_dict, motivo_admissao_dict, diagnostico_dict)
    hospitais_server.hospitais_server('hospitais', indicadores_df)
    dispositivos_server.dispositivos_server('dispositivos',dispositivos_df)


app = App(app_ui, server)