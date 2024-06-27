from shiny import ui, module

@module.ui
def microbiologia_ui(microrganismos_dict):

    return ui.card(
        
        ui.input_slider(
        "slider_age", "Idade", min=0, 
        max=120, value=[0, 120]),

        ui.input_selectize(  
        "selectize",  
        "Microrganismos",  
        microrganismos_dict,  
        multiple=True),

        ui.output_data_frame(id="tabela_teste")
    )
