from shiny import Inputs, Outputs, Session, module, render


@module.server
def dispositivos_server(input: Inputs, output: Outputs, session: Session, dispositivos_df):
    @render.data_frame
    def tabela_dispositivos():
        return render.DataGrid(dispositivos_df)