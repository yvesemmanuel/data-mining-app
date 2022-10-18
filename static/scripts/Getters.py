import static.scripts.EmpenhosSalarios as empSal
import static.scripts.EmpenhosServicosInicAntesEmp as empServ
import os
import pandas as pd


def get_filenames(dir_path):
    res = []

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path.split(".")[0])

    return res


def get_servico_emp(municipio):
    df = pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";")
    municipio_num = int(df[df["Municipio"] == municipio].numUJ)
    
    filename = "./static/datasets/outputs2019/" + \
        str(municipio_num) + ".csv"

    return empServ.getSortedEmpenhos(filename)


def get_salario_emp(municipio):
    df = pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";")
    municipio_num = int(df[df["Municipio"] == municipio].numUJ)

    filename = "./static/datasets/outputs2019/" + \
        str(municipio_num) + ".csv"

    return empSal.getSortedEmpenhos(filename)


def get_dados_correspondencia(municipio):
    df0 = pd.read_csv(
        "./static/datasets/correspondencia_fontes/" + municipio + ".txt", sep=";")
    df1 = pd.read_csv(
        "./static/datasets/correspondencia_fontes/" + municipio + " - descrição.txt")

    # tratando dados
    df0.drop(["Unnamed: 5", "Cidade"], axis=1, inplace=True)

    # linhas e colunas
    linhas = []
    colunas = list(df0.columns)
    linhas_validas = df0[df0["CNPJ"].isna() == False]

    for i, row in linhas_validas.iterrows():
        linhas.append(row.tolist())

    idxs = linhas_validas.index.tolist()
    linhas_descricoes = {}

    i = 0
    for j in idxs[1:]:
        linhas_descricoes[i] = [df0.loc[i].tolist()[:2]
                                for i in range(i + 1, j)]
        i = j

    descricoes = list(linhas_descricoes.values())

    descricao_geral = df1.loc[0].tolist()

    return colunas, linhas, descricoes, descricao_geral


def get_lista_UOFR(municipio):
    df = pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";")
    municipio_num = int(df[df["Municipio"] == municipio].numUJ)

    path = "./static/datasets/outputs2019/" + str(municipio_num) + ".csv"
    df = pd.read_csv(path, sep=',', usecols=['NUMERO_EMPENHO', 'NOME_FONTE_REC', 'NOME_UO'])

    df.rename(columns = {'NOME_FONTE_REC':"FONTE_REC", 'NOME_UO':"UNID_ORC"},  inplace = True)

    return (df["FONTE_REC"] + df["UNID_ORC"]).dropna().unique().tolist()