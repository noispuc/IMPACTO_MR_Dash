from shiny.express import input, render, ui
from tabelas.microbiologia import microbiologia
from shiny import ui

ui.input_slider("val", "Slider label", min=0, max=100, value=50)

@render.text
def slider_val():
    return f"Slider value: {input.val()}"

@render.data_frame
def head():
    return microbiologia.get_dataframe()