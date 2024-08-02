from shiny import ui, module

@module.ui
def filtro_microrganismo_ui(microrganismos_dict):

    return ui.input_selectize(  
        "selectize_microrganismos_microbiologia",  
        "Microrganismo",  
        microrganismos_dict,  
        multiple=True)

@module.ui
def filtro_hospitais_ui(hospitais_dict):

    return ui.input_selectize(  
        "selectize_hospitais_microbiologia",  
        "Hospital",  
        hospitais_dict,  
        multiple=True)

@module.ui
def filtro_tipo_hospital_ui():

    return ui.input_selectize(  
            "selectize_tipo_hospital",  
            "Tipo de Hospital",  
            {"Publico": "Público", "Privado": "Privado"},
            multiple=True)

@module.ui
def filtro_motivo_admissao_ui(motivo_admissao_dict):

    return ui.input_selectize(  
            "selectize_motivo_admissao_microbiologia",  
            "Motivo da Admissão",  
            motivo_admissao_dict,  
            multiple=True)


@module.ui
def filtro_diagnostico_ui(diagnostico_dict):
    return ui.input_selectize(  
        "selectize_diagnostico_microbiologia",  
        "Diagnóstico",  
        diagnostico_dict,  
        multiple=True)

@module.ui
def filtro_mfi_ui():
    return ui.input_selectize(  
        "selectize_MFI_microbiologia",  
        "MFI",  
        {"NF": "Non-Frail", "PF": "Pre-Frail", "F": "Frail"},
        multiple=True)

@module.ui
def filtro_saps_ui():
    return ui.input_selectize(  
    "selectize_SAPS_microbiologia",  
    "SAPS",  
    {0: "0-34", 1: "35-54", 2: "55-74", 3: "75-95", 4: ">95"},
    multiple=True)

@module.ui
def filtro_idade_ui():
    return ui.input_slider(
    "slider_age", "Idade", min=18, 
    max=120, value=[18, 120])