from shiny import App, reactive, render, ui
from antimicrobiano_processamento.py import dataframe

app_ui = ui.page_fluid(
    ui.output_data_frame("tabela_atbs_original"),
    ui.output_data_frame("tabela_atbs_nova")
)

def server(input, output, session):
    @reactive.Calc
    def dados():
        df_final, df_novo = dataframe()
        return df_final, df_novo

    @output
    @render.data_frame
    def tabela_atbs_original():
        df_final, _ = dados()
        return df_final

    @output
    @render.data_frame
    def tabela_atbs_nova():
        _, df_novo = dados()
        return df_novo

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
