from shiny import Inputs, Outputs, Session, module, render
from processamento import hospitais_processamento

@module.server
def hospitais_server(input: Inputs, output: Outputs, session: Session, indicadores_df):
    @render.data_frame
    def tabela_indicadores():
        return render.DataGrid(indicadores_df)
