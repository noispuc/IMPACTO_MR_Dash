from shiny import Inputs, Outputs, Session, reactive, render, module
from processamento import antimicrobiano_processamento

@module.server
def antimicrobiano_server(input: Inputs, output: Outputs, session: Session, df_final, df_descritivo):

    @render.data_frame
    def tabela_atbs_descritiva():
        return render.DataGrid(df_descritivo)
