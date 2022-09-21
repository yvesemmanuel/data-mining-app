import pandas as pd
from statistics import mean
from os.path import exists
from os import makedirs
import static.scripts.Constantes as Constantes


class UJsProcessadas:

    def openFileUJ(ano, numUJ):
        dfUJ = pd.read_csv("./static/datasets/outputs" + str(ano)+"/"+str(numUJ)+".csv")

        return dfUJ

    def selectRowsUJ(valorEmpenho, clausulaValEmp, clausulaCPFouCNPJ, dfUJ):
        dfRes = dfUJ

        if (clausulaValEmp != Constantes.uiClausulaValEmpIndiferente):

            if (clausulaValEmp == Constantes.uiClausulaValEmpMaior):
                dfRes = dfUJ[dfUJ[Constantes.colLiqValorempenho]
                             >= float(valorEmpenho)]
            elif (clausulaValEmp == Constantes.uiClausulaValEmpMenor):
                dfRes = dfUJ[dfUJ[Constantes.colLiqValorempenho]
                             <= float(valorEmpenho)]

        if (clausulaCPFouCNPJ == Constantes.uiCPF):
            dfRes = dfRes[dfRes["CPF_CNPJ"] <= 99999999999]
        elif (clausulaCPFouCNPJ == Constantes.uiCNPJ):
            dfRes = dfRes[dfRes["CPF_CNPJ"] > 99999999999]

        return dfRes

    def getScoreUJ(UJ, ano, numUJ, valorEmpenho, clausulaValEmp, clausulaCPFouCNPJ, limiteAtraso, ordenacaoScore):
        caminhoDoDir = str(ano)+"-"+str(int(valorEmpenho))+"-"+clausulaValEmp+"-"+clausulaCPFouCNPJ+"-"+str(limiteAtraso)

        if not exists("./static/datasets/cache_scores"):
            makedirs("./static/datasets/cache_scores")

        if not exists("./static/datasets/cache_scores/" + caminhoDoDir):
            makedirs("./static/datasets/cache_scores/" + caminhoDoDir)

        if exists("./static/datasets/cache_scores/" + caminhoDoDir + "/all_scores.csv"):
            return True
        elif exists("./static/datasets/cache_scores/"+caminhoDoDir+"/"+str(numUJ)+".csv"):
            return False

        dfUJ = UJsProcessadas.openFileUJ(ano, numUJ)
        dfRes = UJsProcessadas.selectRowsUJ(
            valorEmpenho, Constantes.uiClausulaValEmpMaior, clausulaCPFouCNPJ, dfUJ)
        dfRes = dfRes[dfRes["DIFF_LIQ_PAG"] > limiteAtraso]

        dfGroup = dfRes

        dfGroup = dfGroup.groupby(
            by=["NOME_FONTE_REC", "NOME_UO"], dropna=False).mean()

        arrUJ = []
        arrFonte = []
        arrUO = []
        arrTotalPags = []
        arrTotalPagsAtr = []
        arrScores = []

        for a in dfGroup.index:

            arrFonte.append(a[0])
            arrUO.append(a[1])
            arrTotalPagsAtr.append(
                len(dfRes[(dfRes["NOME_FONTE_REC"] == a[0]) & (dfRes["NOME_UO"] == a[1])]))
            arrUJ.append(numUJ)

            totalPagsUO = len(
                dfUJ[(dfUJ["NOME_FONTE_REC"] == a[0]) & (dfUJ["NOME_UO"] == a[1])])
            arrTotalPags.append(totalPagsUO)

            df = dfRes[(dfRes["NOME_FONTE_REC"] == a[0])
                        & (dfRes["NOME_UO"] == a[1])]
            somaAtrasos = sum(list(df["DIFF_LIQ_PAG"]))
            score = somaAtrasos/30
            score = score/max(totalPagsUO, 1)
            arrScores.append(score)

        NUM_UJ = pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";")

        d = {"NUM_UJ": arrUJ, "Municipio": UJ, "NOME_FONTE": arrFonte, "NOME_UO": arrUO, "totalPagsUO": arrTotalPags,
                "totalPagsAtrasadosUO": arrTotalPagsAtr, "Score": arrScores}
        dfRetorno = pd.DataFrame(data=d)

        dfRetorno.to_csv("./static/datasets/cache_scores/"+caminhoDoDir+"/"+str(numUJ)+".csv", index=False)

        return False

        # lScores = list(dfRetorno["Score"])

        # caminho_completo = "./static/datasets/cache_scores/" + caminhoDoDir

        # if (ordenacaoScore == Constantes.uiOrdenacaoScorePior):
        #     return max(lScores), caminhoDoDir
        # else:
        #     return mean(lScores), caminhoDoDir