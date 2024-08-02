from shiny import ui, module
from shinywidgets import output_widget

from ui.filtros_ui import filtro_microrganismo_ui

@module.ui
def microbiologia_ui(microrganismos_dict, hospitais_dict, motivo_admissao_dict, diagnostico_dict):
    return ui.layout_sidebar(
            ui.sidebar(
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
                "selectize_tipo_hospital",  
                "Tipo de Hospital",  
                {"Publico": "Público", "Privado": "Privado"},
                multiple=True),

                ui.input_selectize(  
                "selectize_motivo_admissao_microbiologia",  
                "Motivo da Admissão",  
                motivo_admissao_dict,  
                multiple=True),

                ui.input_selectize(  
                "selectize_diagnostico_microbiologia",  
                "Diagnóstico",  
                diagnostico_dict,  
                multiple=True),

                ui.input_selectize(  
                "selectize_MFI_microbiologia",  
                "MFI",  
                {"NF": "Non-Frail", "PF": "Pre-Frail", "F": "Frail"},
                multiple=True),

                ui.input_selectize(  
                "selectize_SAPS_microbiologia",  
                "SAPS",  
                {0: "0-34", 1: "35-54", 2: "55-74", 3: "75-95", 4: ">95"},
                multiple=True),

                ui.input_slider(
                "slider_age", "Idade", min=18, 
                max=120, value=[18, 120]),
            ),
            ui.card(
                ui.card_header("Frequência de Identificação de Microrganismos"),
                ui.output_data_frame(id="tabela_frequencia_microrganismo"),
                ui.download_button("download_tabela_frequencia_microrganismo", "Baixar Tabela"),
            ),


            ui.card(
                ui.card_header("Frequência de Microrganismos Resistentes"),
                ui.navset_pill(
                    ui.nav_panel("Gráfico", output_widget("grafico_microrganismos_resistentes")),
                    ui.nav_panel("Tabela", ui.output_data_frame(id="tabela_microrganismos_resistentes")),
                    id="freq_resistente_pill",  
                ),
            ),
    )
