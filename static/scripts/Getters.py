import static.scripts.EmpenhosSalarios as empSal
import static.scripts.EmpenhosServicosInicAntesEmp as empServ
import os
import pandas as pd
from static.scripts.utils import format_cnpj_cpf


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

    filename = './static/datasets/outputs' + ano + '/' + \
        str(municipio_num) + '.csv'

    return empSal.getSortedEmpenhos(filename)


def get_dados_correspondencia(municipio):
    df0 = pd.read_csv('./static/datasets/correspondencia_fontes/' + municipio + ' - descrição.txt')

    # rows and cols
    rows_general_description = df0.loc[0].tolist()
    cols_general_description = df0.loc[0].index.values.tolist()
    
    
    df1 = pd.read_csv('./static/datasets/correspondencia_fontes/tratado_' + municipio + '.csv')

    modals = df1['modal'].dropna().tolist()
    df1.drop('modal', axis=1, inplace=True)

    cols = list(df1.columns)
    rows = [row.tolist() for _, row in df1.iterrows()]

    return cols, rows, cols_general_description, rows_general_description, modals


def get_lista_UOFR(municipio, ano):
    df = pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";")
    municipio_num = int(df[df["Municipio"] == municipio].numUJ)

    if ano == '2020':
        path = "./static/datasets/outputs2020/" + str(municipio_num) + ".csv"
        df = pd.read_csv(path, sep=',', usecols=['NUMERO_EMPENHO', 'NOME_FONTE_REC', 'NOME_UO'])

        df.rename(columns = {'NOME_FONTE_REC':"FONTE_REC", 'NOME_UO':"UNID_ORC"},  inplace = True)

        return (df["FONTE_REC"] + df["UNID_ORC"]).dropna().unique().tolist()
    else:
        path = "./static/datasets/outputs2019/" + str(municipio_num) + ".csv"
        df = pd.read_csv(path, sep=',', usecols=['NUMERO_EMPENHO', 'NOME_FONTE_REC', 'NOME_UO'])

        df.rename(columns = {'NOME_FONTE_REC':"FONTE_REC", 'NOME_UO':"UNID_ORC"},  inplace = True)

        return (df["FONTE_REC"] + df["UNID_ORC"]).dropna().unique().tolist()