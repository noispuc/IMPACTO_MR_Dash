from shiny import ui, module, Inputs
from shinywidgets import output_widget
import faicons

from ui.filtros_ui import filtro_microrganismo_ui

@module.ui
def microbiologia_ui(microrganismos_dict, hospitais_dict, motivo_admissao_dict, diagnostico_dict, estados_dict):
    return ui.layout_sidebar(
            ui.sidebar(
                ui.input_selectize(  
                "selectize_microrganismos_microbiologia",  
                "Microrganismo",  
                microrganismos_dict,  
                multiple=True),

                ui.input_selectize(  
                "selectize_tipo_hospital_microbiologia",  
                "Tipo de Hospital",  
                {"Público": "Público", "Privado": "Privado"},
                multiple=True),

                ui.input_selectize(  
                "selectize_hospitais_microbiologia",  
                "Hospital",  
                hospitais_dict,  
                multiple=True),

                ui.input_selectize(  
                "selectize_regiao_microbiologia",  
                "Região",  
                {"Norte": "Norte", "Nordeste": "Nordeste", "Centro-oeste": "Cento-oeste", 
                 "Sudeste": "Sudeste", "Sul": "Sul"},
                multiple=True),

                ui.input_selectize(  
                "selectize_estado_microbiologia",  
                "Estado",  
                estados_dict,  
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
                "selectize_amostra_microbiologia",  
                "Amostra",  
                {'Sangue':'Sangue', 'Urina':'Urina', 'Respiratório':'Respiratório', 
                 'Swab retal':'Swab retal', 'Swab Nasal':'Swab Nasal', 'Outros Swab':'Outros Swab', 'Outros':'Outros'},  
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
                "slider_age_microbiologia", "Idade", min=18, 
                max=120, value=[18, 120]),

            ),
            ui.layout_columns(
                ui.value_box(
                    title="Número de Pacientes",
                    showcase=faicons.icon_svg("person", width="50px"),
                    value=ui.output_ui("display_num_pacientes_microbiologia"),  
                    theme="text-green",
                ),
                ui.value_box(
                    title="Número de Microrganismos",
                    showcase=faicons.icon_svg("disease", width="50px"),
                    value=ui.output_ui("display_num_microrganismos_microbiologia"),  
                    theme="bg-gradient-orange-red",
                ),
                ui.value_box(
                    title="Número de Hospitais",
                    showcase=faicons.icon_svg("hospital", width="50px"),
                    value=ui.output_ui("display_num_hospitais_microbiologia"),  
                    theme="bg-gradient-blue-purple",
                ),
            ),
            ui.card(
                ui.card_header("Frequência de Identificação de Microrganismos"),
                ui.navset_pill(
                    ui.nav_panel("Tabela", ui.output_data_frame(id="tabela_frequencia_microrganismo"), 
                                 ui.download_button("download_tabela_frequencia_microrganismo", "Baixar Tabela"),),
                    ui.nav_panel("Gráfico", output_widget("grafico_frequencia_microrganismo")),
                    id="freq_ident_pill",  
                ),
                id='freq_ident_card'
            ),

            ui.card(
                ui.card_header("Frequência de Microrganismos Resistentes"),
                ui.navset_pill(
                    ui.nav_panel("Gráfico", output_widget("grafico_microrganismos_resistentes")),
                    ui.nav_panel("Tabela", ui.output_data_frame(id="tabela_microrganismos_resistentes")),
                    id="freq_resistente_pill",  
                ),
                id='freq_resistente_card'
            ),
    )