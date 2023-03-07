import static.scripts.EmpenhosSalarios as empSal
import static.scripts.EmpenhosServicosInicAntesEmp as empServ
from static.scripts.UtilsUJsProcessadas import UJsProcessadas
import os
import pandas as pd
import json
from ast import literal_eval
import static.scripts.Constantes as Constantes
import datetime


def get_delay_sources(selected_year, selected_city_num, limite_atraso, tipo_empenho, tipo_fornecedor):
    df_selected = UJsProcessadas.openFileUJ(selected_year, selected_city_num)

    df_original = df_selected

    df_selected = df_selected.loc[(df_selected["DIFF_LIQ_PAG"] > int(limite_atraso)) & (df_selected["DIFF_LIQ_PAG"] < 5000)]

    if (tipo_fornecedor == Constantes.ui_forn_cnpj):
        df_selected = df_selected.loc[df_selected["CPF_CNPJ"] > 199999999999]
    elif (tipo_fornecedor == Constantes.ui_forn_cpf):
        df_selected = df_selected.loc[
            (df_selected["CPF_CNPJ"] < 199999999999) & (df_selected["CPF_CNPJ"] > 99999999)]
    else:
        df_selected = df_selected.loc[(df_selected["CPF_CNPJ"] > 99999999)]

    if (tipo_empenho == Constantes.ui_emp_lic and int(selected_year) == 2020):
        dfUJ_1 = df_selected.loc[(df_selected["VALOR_EMPENHO"] >= Constantes.vl_disp_lic) & (
                df_selected['DATA_EMP'] < datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]
        dfUJ_2 = df_selected.loc[(df_selected["VALOR_EMPENHO"] >= Constantes.vl_disp_lic_calamidade) & (
                df_selected['DATA_EMP'] >= datetime.strptime(Constantes.inicio_calamidade_2020,
                                                             '%d-%m-%Y'))]

        dfUJ_1 = dfUJ_1.append(dfUJ_2)
        df_selected = dfUJ_1

    elif (tipo_empenho == Constantes.ui_emp_disp and int(selected_year) == 2020):
        dfUJ_1 = df_selected.loc[(df_selected["VALOR_EMPENHO"] < Constantes.vl_disp_lic) & (
                df_selected['DATA_EMP'] < datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]
        dfUJ_2 = df_selected.loc[(df_selected["VALOR_EMPENHO"] < Constantes.vl_disp_lic_calamidade) & (
                df_selected['DATA_EMP'] >= datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]

        dfUJ_1 = dfUJ_1.append(dfUJ_2)
        df_selected = dfUJ_1
    elif (tipo_empenho == Constantes.ui_emp_lic and int(selected_year) == 2019):
        df_selected = df_selected.loc[(df_selected["VALOR_EMPENHO"] >= Constantes.vl_disp_lic)]
    elif (tipo_empenho == Constantes.ui_emp_disp and int(selected_year) == 2019):
        df_selected = df_selected.loc[(df_selected["VALOR_EMPENHO"] < Constantes.vl_disp_lic)]


    list_uos_fontes = []

    for idx,row in df_original.iterrows():
        if((row['NOME_FONTE_REC']+";"+row["NOME_UO"]) not in list_uos_fontes):
            list_uos_fontes.append((row['NOME_FONTE_REC']+";"+row["NOME_UO"]))

    arrUJ = []
    arrFonte = []
    arrUO = []
    arrTotalPags = []
    arrTotalPagsAtr = []
    arrScores = []

    for c in list_uos_fontes:

        lc = c.split(";")

        if(lc[0] != "NI"):
            arrFonte.append(lc[0])
            arrUO.append(lc[1])
            totalPagsUO = len(df_original[(df_original["NOME_FONTE_REC"] == lc[0]) & (df_original["NOME_UO"] == lc[1])])
            arrTotalPags.append(totalPagsUO)

            df = df_selected[(df_selected["NOME_FONTE_REC"] == lc[0]) & (df_selected["NOME_UO"] == lc[1])]
            somaAtrasos = sum(list(df["DIFF_LIQ_PAG"]))
            arrTotalPagsAtr.append(len(list(df["DIFF_LIQ_PAG"])))
            score = somaAtrasos / 30
            score = score / totalPagsUO
            arrScores.append(score)

    d = {"NOME_FONTE_REC": arrFonte, "NOME_UO": arrUO, "totalPagsUO": arrTotalPags,
          "score": arrScores, "totalPagsAtr":arrTotalPagsAtr}
    dfRetorno = pd.DataFrame(data=d)


    #media = sum(arrScores)/len(arrScores)

    dfRetorno.sort_values(by='score', ascending=False, inplace=True)

    options_loans = []
    for idx, row in dfRetorno.iterrows():
        options_loans.append("({:2.5f})".format(row["score"])+" ["+str(row['totalPagsAtr'])+"/" + str(row["totalPagsUO"]) + "] + " +row["NOME_UO"]+" + "+row["NOME_FONTE_REC"])

    # for _, row in df_selected.iterrows():
    #     somaAtrasos = row["DIFF_LIQ_PAG"]
    #     score = somaAtrasos / 30
    #
    #     totalPagsUO = len(df_selected[(row['NOME_FONTE_REC'] == df_selected['NOME_FONTE_REC']) & (row['NOME_UO'] == df_selected['NOME_UO'])])
    #     score = score / totalPagsUO
    #
    #     loan = row['NOME_UO'] + ' + ' + row['NOME_FONTE_REC'] + ' + ({})'.format(score)
    #
    #     if loan not in options_loans:
    #         options_loans.append(loan)


    return options_loans

def get_pagamentos_atrasados(selected_year, selected_city_num, limite_atraso, tipo_empenho, tipo_fornecedor, uo, fonte_rec):
    df_selected = UJsProcessadas.openFileUJ(selected_year, selected_city_num)


    df_selected = df_selected.loc[(df_selected["NOME_UO"] == uo) & (df_selected["NOME_FONTE_REC"] == fonte_rec)]

    df_selected = df_selected.loc[(df_selected["DIFF_LIQ_PAG"] > int(limite_atraso)) & (df_selected["DIFF_LIQ_PAG"] < 5000)]

    df_selected['DATA_EMP'] = pd.to_datetime(df_selected['DATA_EMP'], format='%Y-%m-%d')
    df_selected['DATA'] = pd.to_datetime(df_selected['DATA'], format='%Y-%m-%d')
    df_selected['DATA_LIQ'] = pd.to_datetime(df_selected['DATA'], format='%Y-%m-%d')

    if (tipo_fornecedor == Constantes.ui_forn_cnpj):
        df_selected = df_selected.loc[df_selected["CPF_CNPJ"] > 199999999999]
    elif (tipo_fornecedor == Constantes.ui_forn_cpf):
        df_selected = df_selected.loc[
            (df_selected["CPF_CNPJ"] < 199999999999) & (df_selected["CPF_CNPJ"] > 99999999)]
    else:
        df_selected = df_selected.loc[(df_selected["CPF_CNPJ"] > 99999999)]

    if (tipo_empenho == Constantes.ui_emp_lic and int(selected_year) == 2020):
        dfUJ_1 = df_selected.loc[(df_selected["VALOR_EMPENHO"] >= Constantes.vl_disp_lic) & (
                df_selected['DATA_EMP'] < datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]
        dfUJ_2 = df_selected.loc[(df_selected["VALOR_EMPENHO"] >= Constantes.vl_disp_lic_calamidade) & (
                df_selected['DATA_EMP'] >= datetime.strptime(Constantes.inicio_calamidade_2020,
                                                             '%d-%m-%Y'))]

        dfUJ_1 = dfUJ_1.append(dfUJ_2)
        df_selected = dfUJ_1

    elif (tipo_empenho == Constantes.ui_emp_disp and int(selected_year) == 2020):
        dfUJ_1 = df_selected.loc[(df_selected["VALOR_EMPENHO"] < Constantes.vl_disp_lic) & (
                df_selected['DATA_EMP'] < datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]
        dfUJ_2 = df_selected.loc[(df_selected["VALOR_EMPENHO"] < Constantes.vl_disp_lic_calamidade) & (
                df_selected['DATA_EMP'] >= datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]

        dfUJ_1 = dfUJ_1.append(dfUJ_2)
        df_selected = dfUJ_1
    elif (tipo_empenho == Constantes.ui_emp_lic and int(selected_year) == 2019):
        df_selected = df_selected.loc[(df_selected["VALOR_EMPENHO"] >= Constantes.vl_disp_lic)]
    elif (tipo_empenho == Constantes.ui_emp_disp and int(selected_year) == 2019):
        df_selected = df_selected.loc[(df_selected["VALOR_EMPENHO"] < Constantes.vl_disp_lic)]

    df_selected["FORNECEDOR"] = df_selected["FORNEC"]
    df_selected["ATRASO"] = df_selected["DIFF_LIQ_PAG"]
    df_selected["DATA_PAG"] = df_selected["DATA"]

    return df_selected


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



def get_salario_emp_teste(municipio, ano):

    import os
    print(os.getcwdb())

    #standalone
    df = pd.read_csv('../../static/datasets/ListaMunicipios.csv', sep=';')

    #servidor web
    #df = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')
    print(df.head())
    print(df[df['Municipio'] == municipio].numUJ)
    municipio_num = int(df[df['Municipio'] == municipio].numUJ)

    filename = '../../static/datasets/outputs' + ano + '/' + \
               str(municipio_num) + '.csv'
    # filename = './static/datasets/outputs' + ano + '/' + \
    #     str(municipio_num) + '.csv'

    return empSal.getSortedEmpenhos(filename)

# a = get_salario_emp_teste('Abreu e Lima','2019')
#
# print(a[0])


def get_dados_correspondencia(municipio):
    df0 = pd.read_csv('./static/datasets/correspondencia_fontes/' + municipio + ' - description.txt')

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