from shiny import ui, module

@module.ui
def dispositivos_ui():

    return ui.card(      

        ui.output_data_frame(id="tabela_dispositivos")
    )
