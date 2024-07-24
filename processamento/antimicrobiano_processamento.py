import pandas as pd

def dataframe():
    df_atbs = pd.read_csv("D:\MDR\MDR_Impacto_MR\data\Antimicrobiano.csv ", delimiter=";", encoding='latin1')
    df_admissao = pd.read_csv("D:\MDR\MDR_Impacto_MR\data\Admissao.csv", delimiter=",", encoding='latin1')
    df_desfecho = pd.read_csv("D:\MDR\MDR_Impacto_MR\data\Desfecho.csv", delimiter=";", encoding='latin1')

    df_admissao['id_internacao'] = df_admissao['id_paciente'].astype(str) + "_" + df_admissao.index.astype(str)

    num_atbs = df_atbs["antimicrobial_type_name"].value_counts()

    media = df_atbs.groupby('antimicrobial_type_name')['tempo_uso'].mean().round(2)

    df_admissao_desfecho = pd.merge(df_admissao, df_desfecho, on="id_paciente")

    df_admissao_desfecho["tempo_internacao"] = df_admissao_desfecho["unit_length_stay"]

    tempo_total_internacao = df_desfecho["unit_length_stay"].sum()
    print(f"Tempo total de internação (em dias): {tempo_total_internacao}")

    combined_df = pd.merge(df_atbs, df_admissao_desfecho, on="id_paciente", how='right')

    group_atb = combined_df.groupby('antimicrobial_type_name').agg({
        'tempo_internacao': 'sum',
        'tempo_uso': 'sum'
    })

    group_atb['DOT_atb'] = group_atb['tempo_uso'] / group_atb['tempo_internacao']

    dot_numerador = df_atbs.groupby('antimicrobial_type_name')['tempo_uso'].sum()

    dot_denominador = tempo_total_internacao
    new_dot = (dot_numerador / dot_denominador) * 1000

    new_dot = new_dot.reindex(group_atb.index, fill_value=0)

    group_atb['DOT'] = new_dot.values

    group_atb = group_atb.round(2)

    classificacao_oms = {
        'Amikacin': 'J01GB03',
        'Amoxicilin': 'J01CA04',
        'Amoxicilin / Sulbactam': 'J01CR02',
        'Amoxicillin / Ac. Clavulanic': 'J01CR02',
        'Amphotericin B - Coloidal dispersion': 'J02AA01',
        'Amphotericin B - deoxycholate': 'J02AA01',
        'Amphotericin B - lipid complex': 'J02AA01',
        'Amphotericin B - liposomal': 'J02AA01',
        'Ampicilin': 'J01CA01',
        'Ampicillin / sulbactam': 'J01CR01',
        'Anidulafungin': 'J02AX06',
        'Azithromycin': 'J01FA10',
        'Aztreonam': 'J01DF01',
        'Aztreonam-Avibactam': 'J01DF01',
        'Benzylpenicilin': 'J01CE01',
        'Caspofungin': 'J02AX04',
        'Cefadroxil': 'J01DB05',
        'Cefazolin': 'J01DB04',
        'Cefepime': 'J01DE01',
        'Ceftazidime': 'J01DD02',
        'Ceftazidime / Avibactam': 'J01DD52',
        'Ceftazidime / Sulbactam': 'J01DD02',
        'Ceftolozano / Tazobactam': 'J01DI54',
        'Ceftriaxona': 'J01DD04',
        'Cefuroxime': 'J01DC02',
        'Cefuroxime axetil': 'J01DC02',
        'Cephalexin': 'J01DB01',
        'Cephalothin': 'J01DB03',
        'Cetoconazole': 'J02AB02',
        'Ciprofloxacin': 'J01MA02',
        'Clarithromycin': 'J01FA09',
        'Clindamycin': 'J01FF01',
        'Daptomycin': 'J01XX09',
        'Doxycycline': 'J01AA02',
        'Ertapenem': 'J01DH03',
        'Erythromycin': 'J01FA01',
        'Ethambutol': 'J04AM06',
        'Fluconazole': 'J02AC01',
        'Gentamicin': 'J01GB03',
        'Imipenem-cilastatin': 'J01DH51',
        'Isoniazid': 'J04AM06',
        'Itraconazole': 'J02AC02',
        'Levofloxacin': 'J01MA12',
        'Linezolid': 'J01XX08',
        'Meropenem': 'J01DH02',
        'Meropenem-Vaborbactam': 'J01DH02',
        'Metronidazole': 'J01XD01',
        'Micafungin': 'J02AX05',
        'Moxifloxacin': 'J01MA14',
        'Nitrofurantoin': 'J01XE01',
        'Norfloxacin': 'J01MA06',
        'Oxacillin': 'J01CF04',
        'Piperacillin / Tazobactam': 'J01CR05',
        'Pirazinamid': 'J04AM06',
        'Polymyxin B': 'J01XB02',
        'Posaconazole': 'J02AC04',
        'Rifampicin': 'J04AB02',
        'Sulfadiazine': 'J01EC02',
        'Sulfamethoxazole': 'J01EE04',
        'Sulfamethoxazole / Trimethoprim': 'J01EE04',
        'Teicoplanin': 'J01XA02',
        'Tetracycline': 'J01AA07',
        'Ticarcillin / clavulanate': 'J01CR03',
        'Tigecycline': 'J01AA12',
        'Tobramycin': 'J01GB01',
        'Vancomycin': 'J01XA01',
        'Voriconazole': 'J02AC03'
    }

    def classificar_antibiotico_oms(nome):
        for grupo, oms in classificacao_oms.items():
            if nome == grupo or nome in grupo.split(' / '):
                return oms
        return '-'

    group_atb['OMS'] = group_atb.index.map(classificar_antibiotico_oms)

    classificacao_geral = {
        'Tetraciclinas': ['Doxycycline', 'Tetracycline', 'Tigecycline'],
        'Agentes sistêmicos': ['Amphotericin B', 'Ketoconazole', 'Fluconazole', 'Itraconazole', 'Voriconazole', 'Posaconazole', 'Caspofungin', 'Micafungin', 'Anidulafungin', 'Terbinafine','Cetoconazole'],
        'Tto Tuberculose': ['Rifampicin', 'Rifampicin + isoniazid + pyrazinamide + ethambutol', 'Isoniazid', 'Pyrazinamide', 'Ethambutol','Pirazinamid'],
        'Beta-lactamicos': ['Ampicilin', 'Amoxicillin','Amoxicilin','Benzylpenicilin', 'Penicillin', 'Oxacillin', 'Ampicillin / Sulbactam', 'Amoxicillin / Ac. Clavulanic', 'Ticarcillin / clavulanic acid', 'Piperacillin / tazobactam','Amoxicilin / Sulbactam','Ampicillin / sulbactam','Ticarcillin / clavulanate'],
        'Outros beta-lactamicos': ['Cephalexin', 'Cephalothin', 'Cefazolin', 'Cefadroxil', 'Cefuroxime', 'Ceftriaxone', 'Ceftazidime', 'Cefepime', 'Aztreonam', 'Meropenem', 'Ertapenem', 'Imipenem / cilastatin','Ceftriaxona','Ceftolozano / Tazobactam','Imipenem-cilastatin'],
        'Sulfonamidas': ['Sulfadiazine', 'Sulfamethoxazole / trimethoprim', 'Trimethoprim','Sulfamethoxazole'],
        'Macrolideos': ['Erythromycin', 'Clarithromycin', 'Azithromycin', 'Clindamycin'],
        'Aminoglicosideos': ['Tobramycin', 'Gentamicin', 'Amikacin'],
        'Quinolonas': ['Ciprofloxacin', 'Norfloxacin', 'Levofloxacin', 'Moxifloxacin'],
        'Outros': ['Vancomycin', 'Teicoplanin', 'Colistimethate sodium', 'Polymyxin B', 'Metronidazole', 'Nitrofurantoin', 'Linezolid', 'Daptomycin','Piperacillin / Tazobactam']
    }

    def classificar_antibiotico_geral(nome):
        for grupo, antibs in classificacao_geral.items():
            if any(antib in nome for antib in antibs):
                return grupo
        return '-'

    group_atb['classificacao_geral'] = group_atb.index.map(classificar_antibiotico_geral)

    df_final = pd.DataFrame({
        'antimicrobial_type_name': group_atb.index,
        'classificacao_geral': group_atb['classificacao_geral'].values,
        'OMS': group_atb['OMS'].values,
        'num_atbs': num_atbs.reindex(group_atb.index, fill_value=0).values,
        'media_tempo_uso': media.reindex(group_atb.index, fill_value=0).values,
        'DOT_atb': group_atb['DOT_atb'].values,
        'DOT': group_atb['DOT'].values,
        'dot_numerador': dot_numerador.reindex(group_atb.index, fill_value=0).values,
        'dot_denominador': [dot_denominador] * len(group_atb)
    })

    mediana = combined_df.groupby('antimicrobial_type_name')['tempo_uso'].median().round(2)
    moda = combined_df.groupby('antimicrobial_type_name')['tempo_uso'].agg(lambda x: x.mode()[0]).round(2)
    p75 = combined_df.groupby('antimicrobial_type_name')['tempo_uso'].quantile(0.75).round(2)
    p25 = combined_df.groupby('antimicrobial_type_name')['tempo_uso'].quantile(0.25).round(2)

    df_novo = pd.DataFrame({
        'antimicrobial_type_name': group_atb.index,
        'classificacao_geral': group_atb['classificacao_geral'].values,
        'OMS': group_atb['OMS'].values,
        'media_tempo_uso': media.reindex(group_atb.index, fill_value=0).values,
        'mediana': mediana.reindex(group_atb.index, fill_value=0).values,
        'moda': moda.reindex(group_atb.index, fill_value=0).values,
        'p75': p75.reindex(group_atb.index, fill_value=0).values,
        'p25': p25.reindex(group_atb.index, fill_value=0).values
    })

    #total_pacientes = df_admissao_desfecho['id_internacao'].nunique()
    #print(f"Total de pacientes: {total_pacientes}")


    return df_final, df_novo

df_final, df_novo = dataframe()
