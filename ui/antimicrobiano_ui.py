from shiny import ui, module

@module.ui
def antimicrobiano_ui():

    return ui.card(      

        ui.output_data_frame("tabela_atbs_descritiva")
    )