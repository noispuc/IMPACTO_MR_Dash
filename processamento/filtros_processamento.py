def filtro_saps(dataframe, saps_selecionados):
    if (len(saps_selecionados.get()) > 0):
        if ('0' not in saps_selecionados.get()):
            dataframe = dataframe[dataframe['saps3points'] >= 35]
        if ('1' not in saps_selecionados.get()):
            dataframe = dataframe[~((35 <= dataframe['saps3points']) & (dataframe['saps3points'] <= 54))]
        if ('2' not in saps_selecionados.get()):
            dataframe = dataframe[~((55 <= dataframe['saps3points']) & (dataframe['saps3points'] <= 74))]  
        if ('3' not in saps_selecionados.get()):
            dataframe = dataframe[~((75 <= dataframe['saps3points']) & (dataframe['saps3points'] <= 95))] 
        if ('4' not in saps_selecionados.get()):
            dataframe = dataframe[dataframe['saps3points'] < 95]
    return dataframe

def filtro_microrganismos(dataframe, microrganismos_selecionados, microganismos_dict):
    if (len(microrganismos_selecionados.get()) > 0):
        micro_filtrados = []
        for val in microrganismos_selecionados.get():
            micro_filtrados.append(microganismos_dict[int(val)])
        dataframe = dataframe[dataframe.Microrganismo.isin(micro_filtrados)]
    return dataframe

def filtro_mfi(dataframe, mfi_selecionados):
    if (len(mfi_selecionados.get()) > 0):
        if ('NF' not in mfi_selecionados.get()):
            dataframe = dataframe[dataframe['mfi_points'] != 0]
        if ('PF' not in mfi_selecionados.get()):
            dataframe = dataframe[~dataframe['mfi_points'].isin([1, 2])]
        if ('F' not in mfi_selecionados.get()):
            dataframe = dataframe[dataframe['mfi_points'] < 3] 
    return dataframe