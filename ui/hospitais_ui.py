from shiny import ui, module

@module.ui
def hospitais_ui():

    return ui.card(      

        ui.output_data_frame(id="tabela_indicadores")
    )
