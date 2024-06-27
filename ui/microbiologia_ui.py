from shiny import ui, module

@module.ui
def filtro_idade():

    return ui.input_slider(
        "slider_age", "Idade", min=0, 
        max=120, value=[0, 120])

@module.ui
def filtro_microrganismos(microganismos_dict):
    return ui.input_selectize(  
        "selectize",  
        "Microrganismos",  
        microganismos_dict,  
        multiple=True,  
    ) 
