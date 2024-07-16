from shiny import ui, module

@module.ui
def microbiologia_ui(microrganismos_dict, hospitais_dict, motivo_admissao_dict):

    return ui.card(
        ui.row(

        ui.input_selectize(  
        "selectize_microrganismos_microbiologia",  
        "Microrganismo",  
        microrganismos_dict,  
        multiple=True),

        ui.input_selectize(  
        "selectize_hospitais_microbiologia",  
        "Hospital",  
        hospitais_dict,  
        multiple=True),

        ui.input_selectize(  
        "selectize_motivo_admissao_microbiologia",  
        "Motivo da Admissão",  
        motivo_admissao_dict,  
        multiple=True),

        ui.input_selectize(  
        "selectize_MFI_microbiologia",  
        "MFI",  
        {"NF": "Non-Frail", "PF": "Pre-Frail", "F": "Frail"},
        multiple=True)  

        ),
        ui.input_slider(
        "slider_age", "Idade", min=18, 
        max=120, value=[18, 120]),


        ui.output_data_frame(id="tabela_frequencia_microrganismo"),

        ui.download_button("download_tabela_frequencia_microrganismo", "Baixar Tabela"),
    )
