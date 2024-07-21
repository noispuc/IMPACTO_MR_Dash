from shiny import Inputs, Outputs, Session, module, render
from shinywidgets import render_widget
import plotly.express as px
from processamento import microbiologia_processamento
from datetime import datetime

@module.server
def microbiologia_server(input: Inputs, output: Outputs, session: Session, microbiologia_df, resistentes_df, microganismos_dict, motivo_admissao_dict, diagnosticos_dict):
    
    #DataFrame dos microrganismos
    @render.data_frame
    def tabela_frequencia_microrganismo():
        microrganismos_df = microbiologia_processamento.frequencia_ident_isolados(microbiologia_df, input.slider_age(), 
                                                                                  input.selectize_hospitais_microbiologia, input.selectize_motivo_admissao_microbiologia, 
                                                                                  motivo_admissao_dict, input.selectize_microrganismos_microbiologia, microganismos_dict,
                                                                                  input.selectize_MFI_microbiologia, input.selectize_SAPS_microbiologia,
                                                                                  input.selectize_diagnostico_microbiologia, diagnosticos_dict)
        return render.DataGrid(microrganismos_df)
    

    #Download do DataFrame dos microrganismos
    @render.download(filename=lambda: f"frequencia-micorganismo-{datetime.now()}.csv")
    async def download_tabela_frequencia_microrganismo():
        microrganismos_df = microbiologia_processamento.frequencia_ident_isolados(microbiologia_df, input.slider_age(), 
                                                                                  input.selectize_hospitais_microbiologia, input.selectize_motivo_admissao_microbiologia, 
                                                                                  motivo_admissao_dict, input.selectize_microrganismos_microbiologia, microganismos_dict,
                                                                                  input.selectize_MFI_microbiologia, input.selectize_SAPS_microbiologia, 
                                                                                  input.selectize_diagnostico_microbiologia, diagnosticos_dict)
        yield microrganismos_df.to_csv(index=None, sep=';')


    @render.data_frame
    def tabela_microrganismos_resistentes():
        microrganismos_df = microbiologia_processamento.frequencia_resistentes_update(resistentes_df, input.selectize_microrganismos_microbiologia, microganismos_dict)
        return render.DataGrid(microrganismos_df)
    
    @render_widget
    def grafico_microrganismos_resistentes():
        microrganismos_df = microbiologia_processamento.frequencia_resistentes_update(resistentes_df, input.selectize_microrganismos_microbiologia, microganismos_dict)
        resistentes_plot = px.bar(microrganismos_df, x="infec_coleta_data", y=["resistente", "sensiveis"])
        return resistentes_plot  