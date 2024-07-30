from shiny import App, reactive, render, ui
from antimicrobiano_processamento import dataframe

def server(input, output, session):
    @reactive.Calc
    def dados():
        df_final, df_descritivo = dataframe()
        return df_final, df_descritivo

    @output
    @render.data_frame
    def tabela_atbs_original():
        df_final, _ = dados()
        return df_final

    @output
    @render.data_frame
    def tabela_atbs_nova():
        _, df_descritivo = dados()
        return df_descritivo
