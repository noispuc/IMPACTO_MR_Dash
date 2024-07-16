from shiny import Inputs, Outputs, Session, module, render
from processamento import microbiologia_processamento
from datetime import datetime

@module.server
def microbiologia_server(input: Inputs, output: Outputs, session: Session, microbiologia_df, microganismos_dict, motivo_admissao_dict):
    
    #DataFrame dos microrganismos
    @render.data_frame
    def tabela_frequencia_microrganismo():
        microrganismos_df = microbiologia_processamento.frequencia_ident_isolados(microbiologia_df, input.slider_age(), 
                                                                                  input.selectize_hospitais_microbiologia, input.selectize_motivo_admissao_microbiologia, 
                                                                                  motivo_admissao_dict, input.selectize_microrganismos_microbiologia, microganismos_dict,
                                                                                  input.selectize_MFI_microbiologia)
        return render.DataGrid(microrganismos_df)
    

    #Download do DataFrame dos microrganismos
    @render.download(filename=lambda: f"frequencia-micorganismo-{datetime.now()}.csv")
    async def download_tabela_frequencia_microrganismo():
        microrganismos_df = microbiologia_processamento.frequencia_ident_isolados(microbiologia_df, input.slider_age(), 
                                                                                  input.selectize_hospitais_microbiologia, input.selectize_motivo_admissao_microbiologia, 
                                                                                  motivo_admissao_dict, input.selectize_microrganismos_microbiologia, microganismos_dict,
                                                                                  input.selectize_MFI_microbiologia)
        yield microrganismos_df.to_csv(index=None, sep=';')