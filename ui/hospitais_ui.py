from shiny import ui, module

@module.ui
def hospitais_ui(microrganismos_dict, hospitais_dict, motivo_admissao_dict, diagnostico_dict, estados_dict):

    return ui.layout_sidebar(      
        ui.sidebar(
            ui.input_selectize(  
            "selectize_tipo_hospital_hospitais",  
            "Tipo de Hospital",  
            {"Público": "Público", "Privado": "Privado"},
            multiple=True),

            ui.input_selectize(  
            "selectize_hospitais_hospitais",  
            "Hospital",  
            hospitais_dict,  
            multiple=True),

            ui.input_selectize(  
            "selectize_regiao_hospitais",  
            "Região",  
            {"Norte": "Norte", "Nordeste": "Nordeste", "Centro-oeste": "Cento-oeste", 
                "Sudeste": "Sudeste", "Sul": "Sul"},
            multiple=True),

            ui.input_selectize(
            "selectize_estado_hospitais",  
            "Estado",  
            estados_dict,  
            multiple=True),

            ui.input_selectize(  
            "selectize_motivo_admissao_hospitais",  
            "Motivo da Admissão",  
            motivo_admissao_dict,  
            multiple=True),

            ui.input_selectize(  
            "selectize_diagnostico_hospitais",  
            "Diagnóstico",  
            diagnostico_dict,  
            multiple=True),

            ui.input_selectize(  
            "selectize_amostra_hospitais",  
            "Amostra",  
            {'Sangue':'Sangue', 'Urina':'Urina', 'Respiratório':'Respiratório', 
                'Swab retal':'Swab retal', 'Swab Nasal':'Swab Nasal', 'Outros Swab':'Outros Swab', 'Outros':'Outros'},  
            multiple=True),

            ui.input_selectize(  
            "selectize_MFI_hospitais",  
            "MFI",  
            {"NF": "Non-Frail", "PF": "Pre-Frail", "F": "Frail"},
            multiple=True),

            ui.input_selectize(  
            "selectize_SAPS_hospitais",  
            "SAPS",  
            {0: "0-34", 1: "35-54", 2: "55-74", 3: "75-95", 4: ">95"},
            multiple=True),

            ui.input_slider(
            "slider_age_hospitais", "Idade", min=18, 
            max=120, value=[18, 120]),
        ),
        ui.card(
                ui.card_header("Indicadores de Hospitais"),
                ui.output_data_frame(id="tabela_indicadores"),
                id='indicadores_hosp_card'
            ),
    )
