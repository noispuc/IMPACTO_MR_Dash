from shiny import ui

app_ui = ui.page_fluid(
    ui.output_data_frame("tabela_atbs"),
    ui.output_data_frame("tabela_atbs_descritiva")
)
