from server import microbiologia_server
from ui import microbiologia_ui
from processamento import microbiologia_processamento
from shiny import App, Inputs, ui, Outputs, Session


microganismos_dict = microbiologia_processamento.get_pathogen_type_name()
microbiologia_df = microbiologia_processamento.get_dataframe()


app_ui = ui.page_fluid (
    microbiologia_ui.microbiologia_ui(id="microbiologia", microrganismos_dict=microganismos_dict),
    ) 


def server(input: Inputs, output: Outputs, session: Session):
    microbiologia_server.microbiologia_server("microbiologia", microbiologia_df, microganismos_dict)
    
app = App(app_ui, server)