from shiny import Inputs, Outputs, Session, module, render
from processamento import hospitais_processamento

@module.server
def hospitais_server(input: Inputs, output: Outputs, session: Session, tabela_indicadores):
    @render.data_frame
    def tabela_indicadores():
        
        return render.DataGrid(tabela_indicadores)
