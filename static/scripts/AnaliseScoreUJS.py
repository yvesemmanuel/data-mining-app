import pandas as pd

toleranciaDiasDispensa = 10
toleranciaDiasLicitacao = 30

scoresAtrasoUJ = {}
pagLiqsResultantes = []
resumoPorMunicipio = {}


def computaAtrasos(valorMaximoDispensa, ano):
    global scoresAtrasoUJ
    global pagLiqsResultantes
    global resumoPorMunicipio

    dfPagamentosLiq = pd.read_csv(
        "./static/datasets/outputs"+str(ano)+"/allUJs.csv", sep=",", index_col=False)
    dfPagamentosLiq["UJ"] = dfPagamentosLiq["CIDADE"] + "#" + \
        dfPagamentosLiq["NOME_UO"] + "#" + dfPagamentosLiq["NOME_FONTE_REC"]

    if (valorMaximoDispensa > 0):
        dfPagsLicDisp = dfPagamentosLiq.loc[
            ((dfPagamentosLiq["VALOR_EMPENHO"] <= valorMaximoDispensa) & (dfPagamentosLiq["DIFF_LIQ_PAG"] < 365))]
    else:
        dfPagsLicDisp = dfPagamentosLiq.loc[
            ((dfPagamentosLiq["VALOR_EMPENHO"] > abs(valorMaximoDispensa)) & (dfPagamentosLiq["DIFF_LIQ_PAG"] < 365))]

    pagLiqsResultantes = dfPagsLicDisp

    totalPagamentosUJ = {}

    listTodosMun = list(dfPagamentosLiq["CIDADE"].unique())
    for m in listTodosMun:
        resumoPorMunicipio[m] = {"UJ": [], "UJFormatada": [], "scores": []}

    grouped_df = dfPagamentosLiq.groupby("UJ")
    for key, _ in grouped_df:
        totalPagamentosUJ[grouped_df.get_group(key).iloc[0]["UJ"]] = len(
            grouped_df.get_group(key))
        scoresAtrasoUJ[grouped_df.get_group(key).iloc[0]["UJ"]] = 0.0

    toleranciaDias = 0
    if (valorMaximoDispensa > 0):
        toleranciaDias = toleranciaDiasDispensa
    else:
        toleranciaDias = toleranciaDiasLicitacao

    dfPagsLicDisp = dfPagsLicDisp.loc[(
        dfPagsLicDisp["DIFF_LIQ_PAG"] > toleranciaDias)]

    listUJs = list(totalPagamentosUJ.keys())
    ctPags = 0

    for uj in listUJs:
        pagsUJ = dfPagsLicDisp.loc[dfPagsLicDisp["UJ"] == uj]

        sumAtrasos = 0

        listAtrasos = list(pagsUJ["DIFF_LIQ_PAG"])
        totalAtrasos = 0
        for atr in listAtrasos:
            totalAtrasos += atr
            sumAtrasos += 1 + ((atr - toleranciaDias) / 30)
            ctPags += 1

        scoresAtrasoUJ[uj] = sumAtrasos / totalPagamentosUJ[uj]

        lUj = uj.split("#")
        mun = lUj[0]
        resumoPorMunicipio[mun]["UJ"].append(uj)
        resumoPorMunicipio[mun]["scores"].append(scoresAtrasoUJ[uj])
        resumoPorMunicipio[mun]["UJFormatada"].append(
            "("+lUj[0] + ")"+" "+lUj[1]+" *** "+lUj[2] + " ("+"{:.3f}".format(scoresAtrasoUJ[uj])+")")

        if (len(pagsUJ) == 0):
            scoresAtrasoUJ[uj] = 0

    return scoresAtrasoUJ


def getListaMunicipios(ano):
    dfPagamentosLiq = pd.read_csv(
        "outputs" + str(ano) + "/allUJs.csv", sep=",", index_col=False)
    listaMunicipios = list(dfPagamentosLiq["CIDADE"].unique())

    return listaMunicipios


def getScoresUJ():
    return scoresAtrasoUJ


def getPagLiqsRes():
    return pagLiqsResultantes


def getUJsPorMunicipio(municipio):
    df = getPagLiqsRes()
    df = df[df["CIDADE"] == municipio]

    listUJS = list(df["UJ"].unique())

    listUJSFormatada = []

    listUJSNaoFormatada = []

    for l in listUJS:
        if ("#" in str(l)):
            listUJSNaoFormatada.append(l)
            s = l.split("#")
            listUJSFormatada.append("(" + s[0] + ") " + s[1] + " -*- " + s[2])

    return listUJSFormatada, listUJSNaoFormatada
