from shiny import Inputs, Outputs, Session, module, render
from processamento import microbiologia_processamento

@module.server
def microbiologia_server(input: Inputs, output: Outputs, session: Session, microbiologia_df, microganismos_dict):
    @render.data_frame
    def tabela_teste():
        microrganismos_df = microbiologia_processamento.frequencia_ident_isolados(microbiologia_df, input.slider_age()) 
        if (len(input.selectize()) > 0):
            micro_filtrados = []
            for val in input.selectize():
                micro_filtrados.append(microganismos_dict['Microrganismos'][int(val)])
            organismos_filter_df = microrganismos_df[microrganismos_df.Microrganismo.isin(micro_filtrados)]
            return render.DataGrid(organismos_filter_df)
        return render.DataGrid(microrganismos_df)

    #@render.data_frame
    #def head2():
        #return render.DataGrid(microbiologia_processamento.isolamento_bacterias_resistentes())