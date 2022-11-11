import pandas as pd
from statistics import mean
from os.path import exists
from datetime import datetime
from . import Constantes


class UJsProcessadas:

    def openFileUJ(ano, numUJ):
        dfUJ = pd.read_csv('./static/datasets/outputs'+str(ano)+'/'+str(numUJ)+'.csv')

        return dfUJ

    def selectRowsUJ(valorEmpenho, clausulaValEmp, clausulaCPFouCNPJ, dfUJ):

        dfRes = dfUJ

        if(clausulaValEmp != Constantes.uiClausulaValEmpIndiferente):

            if(clausulaValEmp == Constantes.uiClausulaValEmpMaior):
                dfRes = dfUJ[dfUJ[Constantes.colLiqValorempenho] >= float(valorEmpenho)]
            elif(clausulaValEmp == Constantes.uiClausulaValEmpMenor):
                dfRes = dfUJ[dfUJ[Constantes.colLiqValorempenho] <= float(valorEmpenho)]


        if(clausulaCPFouCNPJ == Constantes.uiCPF):
            dfRes = dfRes[dfRes["CPF_CNPJ"] <= 99999999999]
        elif(clausulaCPFouCNPJ == Constantes.uiCNPJ):
            dfRes = dfRes[dfRes["CPF_CNPJ"] > 99999999999]

        return dfRes

    def get_pagamentos_atrasados(ano, is_licitacao, is_cpf, limiteAtraso, num_uj, uo, fonte):

        dfUJ = UJsProcessadas.openFileUJ(ano, num_uj)

        dfUJ['DATA_EMP'] = pd.to_datetime(dfUJ['DATA_EMP'], format='%Y-%m-%d')
        dfUJ['DATA'] = pd.to_datetime(dfUJ['DATA'], format='%Y-%m-%d')
        dfUJ['DATA_LIQ'] = pd.to_datetime(dfUJ['DATA'], format='%Y-%m-%d')

        df_consulta = dfUJ.loc[(dfUJ["NOME_UO"] == uo) & (dfUJ["NOME_FONTE_REC"] == fonte)]
        df_consulta = df_consulta.loc[(dfUJ["DIFF_LIQ_PAG"] > limiteAtraso) & (dfUJ["DIFF_LIQ_PAG"] < 5000)]

        if (is_cpf == Constantes.ui_forn_cnpj):
            df_consulta = df_consulta.loc[df_consulta["CPF_CNPJ"] > 199999999999]
        elif (is_cpf == Constantes.ui_forn_cpf):
            df_consulta = df_consulta.loc[
                    (df_consulta["CPF_CNPJ"] < 199999999999) & (df_consulta["CPF_CNPJ"] > 99999999)]
        else:
            df_consulta = df_consulta.loc[(df_consulta["CPF_CNPJ"] > 99999999)]

        if (is_licitacao == Constantes.ui_emp_lic and ano == 2020):
            dfUJ_1 = df_consulta.loc[(df_consulta["VALOR_EMPENHO"] >= Constantes.vl_disp_lic) & (
                            df_consulta['DATA_EMP'] < datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]
            dfUJ_2 = df_consulta.loc[(df_consulta["VALOR_EMPENHO"] >= Constantes.vl_disp_lic_calamidade) & (
                            df_consulta['DATA_EMP'] >= datetime.strptime(Constantes.inicio_calamidade_2020,
                                                                         '%d-%m-%Y'))]

            dfUJ_1 = dfUJ_1.append(dfUJ_2)
            df_consulta = dfUJ_1
        elif (is_licitacao == Constantes.ui_emp_disp and ano == 2020):
            dfUJ_1 = df_consulta.loc[(df_consulta["VALOR_EMPENHO"] < Constantes.vl_disp_lic) & (
                        df_consulta['DATA_EMP'] < datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]
            dfUJ_2 = df_consulta.loc[(df_consulta["VALOR_EMPENHO"] < Constantes.vl_disp_lic_calamidade) & (
                        df_consulta['DATA_EMP'] >= datetime.strptime(Constantes.inicio_calamidade_2020, '%d-%m-%Y'))]

            dfUJ_1 = dfUJ_1.append(dfUJ_2)
            df_consulta = dfUJ_1
        elif (is_licitacao == Constantes.ui_emp_lic and ano == 2019):
            df_consulta = df_consulta.loc[(dfUJ["VALOR_EMPENHO"] >= Constantes.vl_disp_lic)]
        elif (is_licitacao == Constantes.ui_emp_disp and ano == 2019):
            df_consulta = df_consulta.loc[(dfUJ["VALOR_EMPENHO"] < Constantes.vl_disp_lic)]

        col = ["VALOR", "FORNECEDOR", "CPF_CNPJ", "ATRASO",
               "ID_EMPENHO", "DATA_PAG", "DATA_LIQ"]

        df_retorno = pd.DataFrame(columns=col)

        df_retorno["VALOR"] = df_consulta["VALOR"]
        df_retorno["FORNECEDOR"] = df_consulta["FORNEC"]
        df_retorno["CPF_CNPJ"] = df_consulta["CPF_CNPJ"]
        df_retorno["ATRASO"] = df_consulta["DIFF_LIQ_PAG"]
        df_retorno["ID_EMPENHO"] = df_consulta["ID_EMPENHO"]
        df_retorno["DATA_PAG"] = df_consulta["DATA"]
        df_retorno["DATA_LIQ"] = df_consulta["DATA_LIQ"]

        return df_retorno


    def getScoreUJOld(ano, numUJ, valorEmpenho, clausulaValEmp, clausulaCPFouCNPJ, limiteAtraso, ordenacaoScore):

        nomeArquivoCache = str(ano)+"-"+str(numUJ)+"-"+str(int(valorEmpenho))+clausulaValEmp+clausulaCPFouCNPJ+str(limiteAtraso)+".csv"

        if(exists("cache/"+nomeArquivoCache)):
            dfRetorno = pd.read_csv('cache/'+nomeArquivoCache)
        else:
            dfUJ = UJsProcessadas.openFileUJ(ano, numUJ)

            dfRes = UJsProcessadas.selectRowsUJ(valorEmpenho, Constantes.uiClausulaValEmpMaior, clausulaCPFouCNPJ, dfUJ)
            dfRes = dfRes[dfRes["DIFF_LIQ_PAG"] > limiteAtraso]

            dfGroup = dfRes

            dfGroup = dfGroup.groupby(by=["NOME_FONTE_REC", "NOME_UO"], dropna=False).mean()

            arrUJ = []
            arrFonte = []
            arrUO = []
            arrTotalPags = []
            arrTotalPagsAtr = []
            arrScores = []

            for a in dfGroup.index:

                arrFonte.append(a[0])
                arrUO.append(a[1])
                arrTotalPagsAtr.append(len(dfRes[(dfRes["NOME_FONTE_REC"] == a[0]) & (dfRes["NOME_UO"] == a[1])]))
                arrUJ.append(numUJ)

                totalPagsUO = len(dfUJ[(dfUJ["NOME_FONTE_REC"] == a[0]) & (dfUJ["NOME_UO"] == a[1])])
                arrTotalPags.append(totalPagsUO)

                df = dfRes[(dfRes["NOME_FONTE_REC"] == a[0]) & (dfRes["NOME_UO"] == a[1])]
                somaAtrasos = sum(list(df["DIFF_LIQ_PAG"]))
                score = somaAtrasos/30
                score = score/totalPagsUO
                arrScores.append(score)

            d = {"NUM_UJ": arrUJ, "NOME_FONTE": arrFonte, "NOME_UO": arrUO, "totalPagsUO": arrTotalPags,
                 "totalPagsAtrasadosUO": arrTotalPagsAtr, "score": arrScores}
            dfRetorno = pd.DataFrame(data=d)

            dfRetorno.to_csv('./static/datasets/cache_atrasos/'+nomeArquivoCache, index=False)

        lScores = list(dfRetorno["score"])

        if(ordenacaoScore == Constantes.uiOrdenacaoScorePior):
            return max(lScores)
        else:
            return mean(lScores)

    def getNaoConformidades(ano):
        from os import listdir
        from os.path import isfile, join
        mypath = "outputs"+str(ano)+"/"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for f in onlyfiles:
            dfUJ = UJsProcessadas.openFileUJ(ano, mypath+f)