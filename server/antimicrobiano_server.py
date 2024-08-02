from shiny import Inputs, Outputs, Session, reactive, render, module
from processamento import antimicrobiano_processamento

@module.server
def antimicrobiano_server(input: Inputs, output: Outputs, session: Session, df_final, df_descritivo):

    #@render.data_frame
    #def tabela_atbs():
        #return render.DataGrid(df_final)

    @render.data_frame
    def tabela_atbs_descritiva():
        print("Render descritivo")
        return render.DataGrid(df_descritivo)
