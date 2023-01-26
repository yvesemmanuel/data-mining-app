import static.scripts.EmpenhosSalarios as empSal
import static.scripts.EmpenhosServicosInicAntesEmp as empServ
from static.scripts.UtilsUJsProcessadas import UJsProcessadas
import os
import pandas as pd
import json
from ast import literal_eval


def get_delay_sources(selected_year, selected_city_num):
    df_selected = UJsProcessadas.openFileUJ(selected_year, selected_city_num)

    options_loans = []
    for _, row in df_selected.iterrows():
        somaAtrasos = row["DIFF_LIQ_PAG"]
        score = somaAtrasos / 30 # TODO: check a way to add scoring info on tables

        totalPagsUO = len(df_selected[(row['NOME_FONTE_REC'] == df_selected['NOME_FONTE_REC']) & (row['NOME_UO'] == df_selected['NOME_UO'])])
        score = score / totalPagsUO

        loan = row['NOME_UO'] + ' + ' + row['NOME_FONTE_REC'] + ' + ({})'.format(score)

        if loan not in options_loans:
            options_loans.append(loan)


    return options_loans


def get_filenames(dir_path):
    res = []

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path.split(".")[0])

    return res


def get_servico_emp(municipio, ano):
    df = pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";")
    municipio_num = int(df[df["Municipio"] == municipio].numUJ)
    
    filename = "./static/datasets/outputs" + ano + "/" + \
        str(municipio_num) + ".csv"

    return empServ.getSortedEmpenhos(filename)


def get_salario_emp(municipio, ano):
    df = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')
    municipio_num = int(df[df['Municipio'] == municipio].numUJ)

    filename = './static/datasets/outputs' + ano + '/' + str(municipio_num) + '.csv'

    return empSal.getSortedEmpenhos(filename)


def get_dados_correspondencia(municipio):
    df0 = pd.read_csv('./static/datasets/correspondencia_fontes/' + municipio + ' - descrição.txt')

    # rows and cols
    rows_general_description = df0.loc[0].tolist()
    cols_general_description = df0.loc[0].index.values.tolist()
    
    
    df1 = pd.read_csv('./static/datasets/correspondencia_fontes/tratado_' + municipio + '.csv')

    modals = []
    for modal in df1.modal.tolist():
        lst = literal_eval(modal)
        
        new_lst = []
        for item in lst:
            try:
                new_item = literal_eval(item)
            except:
                new_item = item

            new_lst.append(new_item)
    
        modals.append(new_lst)

    df1.drop('modal', axis=1, inplace=True)

    cols = list(df1.columns)
    rows = [row.tolist() for _, row in df1.iterrows()]

    return cols, rows, cols_general_description, rows_general_description, modals


def get_non_conformities(selected_year):
    df = pd.read_csv('./static/datasets/inconformidades/tratado_inconformidades_' + str(selected_year) + '.csv')

    links = df['link'].tolist()
    df = df.drop('link', axis=1)

    cols = list(df.columns)

    rows = []
    for idx, row in df.iterrows():
        new_id = '<a href="{}" target="_blank">{}</a>'.format(links[idx], row['ID'])
        row['ID'] = new_id
        rows.append(row)

    return rows, cols, links
    

def get_lista_UOFR(municipio, ano):
    df = pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";")
    municipio_num = int(df[df["Municipio"] == municipio].numUJ)

    df = pd.read_csv('./static/datasets/outputs{}/{}.csv'.format(ano, municipio_num), sep=',', usecols=['NUMERO_EMPENHO', 'NOME_FONTE_REC', 'NOME_UO'])

    df.rename(columns = {'NOME_FONTE_REC':"FONTE_REC", 'NOME_UO':"UNID_ORC"},  inplace = True)

    return (df["FONTE_REC"] + ' + ' + df["UNID_ORC"]).dropna().unique().tolist()