import pandas
import numpy as np
import datetime

def get_dataframe():
    microbiologia = pandas.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Microbiologia.csv", 
                                    sep=';', encoding='latin-1', low_memory=True, 
                                    usecols=["infec_coleta_data", "pathogen_type_name"], parse_dates=["infec_coleta_data"])
    
    date_before = np.datetime64(datetime.date(2023, 12, 31) - datetime.timedelta(days=90))
    tresMeses = microbiologia[microbiologia['infec_coleta_data'] >= date_before]
    tresMeses = tresMeses.rename(columns={'infec_coleta_data': '3 meses', 'pathogen_type_name': 'Microrganismo'})
    tresMeses = tresMeses.groupby("Microrganismo").count()    
    tresMeses['% 3 meses'] = 100 * tresMeses['3 meses'] / tresMeses['3 meses'].sum()
    tresMeses['% 3 meses'] = tresMeses['% 3 meses'].round(2)
    
    date_before = np.datetime64(datetime.date(2023, 12, 31) - datetime.timedelta(days=180))
    seisMeses = microbiologia[microbiologia['infec_coleta_data'] >= date_before]
    seisMeses = seisMeses.rename(columns={'infec_coleta_data': '6 meses', 'pathogen_type_name': 'Microrganismo'})
    seisMeses = seisMeses.groupby("Microrganismo").count()
    seisMeses['% 6 meses'] = 100 * seisMeses['6 meses'] / seisMeses['6 meses'].sum()
    seisMeses['% 6 meses'] = seisMeses['% 6 meses'].round(2)

    resultado = pandas.merge(tresMeses, seisMeses, how='outer', on='Microrganismo')
    resultado.reset_index(drop=False, inplace=True)
    resultado.fillna(0, inplace=True)
    #print(microbiologia)
    
    return resultado