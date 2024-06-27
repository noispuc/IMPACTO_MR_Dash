from shiny import Inputs, Outputs, Session, module, render
from processamento import microbiologia_processamento

@module.server
def teste(input: Inputs, output: Outputs, session: Session):
    print("Chamado 1")

    @render.data_frame
    def head():
        print("Chamado")
        microganismos_dict = []
        microbiologia_df = []
        microrganismos_df = microbiologia_processamento.frequencia_ident_isolados(microbiologia_df, input.slider_age()) 
        if (len(input.selectize()) > 0):
            micro_filtrados = []
            for val in input.selectize():
                micro_filtrados.append(microganismos_dict['Microrganismos'][int(val)])
            organismos_filter_df = microrganismos_df[microrganismos_df.Microrganismo.isin(micro_filtrados)]
            return render.DataGrid(organismos_filter_df)
        return render.DataGrid(microrganismos_df)

    #@output
    #@render.data_frame
    #def head2():
        #return render.DataGrid(microbiologia_processamento.isolamento_bacterias_resistentes())