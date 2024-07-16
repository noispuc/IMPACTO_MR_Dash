from server import microbiologia_server, hospitais_server
from ui import microbiologia_ui, hospitais_ui
from processamento import microbiologia_processamento, hospitais_processamento
from shiny import App, Inputs, ui, Outputs, Session
import pandas as pd

admissao = pd.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Admissao.csv", 
                                    index_col=["id_paciente", "id_hosp_internacao", "id_uti_internacao"],
                                    sep=';', encoding='latin-1', low_memory=True,)


'''Microbiologia'''
microganismos_dict = microbiologia_processamento.get_microrganismos_dict()
microbiologia_df = microbiologia_processamento.get_microbiologia_df(admissao)
hospitais_dict = microbiologia_processamento.get_hospitais_dict()
motivo_admissao_dict = microbiologia_processamento.get_motivos_admissao_dict(admissao[['admission_reason_name']])


'''Hospitais'''
desfecho_adm = hospitais_processamento.get_desfecho_adm()
microbio = hospitais_processamento.get_microbio()
df_pacientes_dia = hospitais_processamento.get_df_pacientes_dia(desfecho_adm, microbio)
desfecho_juntas = hospitais_processamento.get_desfecho_juntas(desfecho_adm, microbio)
indicadores_df = hospitais_processamento.get_tabela_indicadores(df_pacientes_dia, desfecho_juntas)


''' UI '''
app_ui = ui.page_fluid (
    microbiologia_ui.microbiologia_ui(id="microbiologia", microrganismos_dict=microganismos_dict, hospitais_dict=hospitais_dict, motivo_admissao_dict=motivo_admissao_dict),
    hospitais_ui.hospitais_ui(id='hospitais'),
    ) 


''' SERVER '''
def server(input: Inputs, output: Outputs, session: Session):
    microbiologia_server.microbiologia_server("microbiologia", microbiologia_df, microganismos_dict)
    hospitais_server.hospitais_server('hospitais', indicadores_df)


app = App(app_ui, server)