from server import microbiologia_server
from ui import microbiologia_ui
from processamento import microbiologia_processamento
from shiny import App, Inputs, ui, Outputs, Session


microganismos_dict = microbiologia_processamento.get_pathogen_type_name()
microbiologia_df = microbiologia_processamento.get_dataframe()


app_ui = ui.page_fluid (
    microbiologia_ui.filtro_idade("elem1"),
    microbiologia_ui.filtro_microrganismos("elem1", microganismos_dict),
    ui.output_data_frame(id="head")) 


def server(input: Inputs, output: Outputs, session: Session):
    microbiologia_server.teste("elem1")
    
app = App(app_ui, server)