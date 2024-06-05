from pandas import pandas

def get_dataframe():
    microbiologia = pandas.read_csv("D:/MDR/MDR_Impacto_MR/analysis_impacto_python/impactoMR/data/Microbiologia.csv", 
                                    sep=';', encoding='latin-1', low_memory=True,)
    return microbiologia