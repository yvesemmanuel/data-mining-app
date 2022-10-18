import pandas as pd
from datetime import datetime


def pegaQtdultrapass(item):
    return item[4]


def MudaMunicipio2(index, numero, diastl):
    muniselect = pd.read_csv(index, sep=',', usecols=['NUMERO_EMPENHO',
                                                      'VALOR_EMPENHO', 'DATA', 'CPF_CNPJ',
                                                      'DATA_LIQ', 'VALOR', 'FORNEC', 'ID_PAGAMENTO', 'NOME_FONTE_REC', 'NOME_UO'])

    camposuteismuni = muniselect
    camposuteismuni.rename(columns={'DATA': 'DATA_PAGAMENTO', "VALOR": "VALOR_PAGAMENTO",
                           'NOME_FONTE_REC': "FONTE_REC", 'NOME_UO': "UNID_ORC"},  inplace=True)

    vetorempsagres2 = CriaDivisao2(camposuteismuni, diastl)
    calculo1 = 0
    for k in vetorempsagres2:
        calculo1 += k.retornaIndice()

    return calculo1


def MudaMunicio(numero, uofr, diastl):
    muniselect = pd.read_csv("./static/datasets/outputs2019/" + str(numero) + ".csv", sep=',', usecols=['NUMERO_EMPENHO',
                                                                                                        'VALOR_EMPENHO', 'DATA', 'CPF_CNPJ',
                                                                                                        'DATA_LIQ', 'VALOR', 'FORNEC', 'ID_PAGAMENTO', 'NOME_FONTE_REC', 'NOME_UO'])

    camposuteismuni = muniselect
    camposuteismuni.rename(columns={'DATA': 'DATA_PAGAMENTO', "VALOR": "VALOR_PAGAMENTO",
                           'NOME_FONTE_REC': "FONTE_REC", 'NOME_UO': "UNID_ORC"},  inplace=True)

    empsagres = CriaDivisao(camposuteismuni, diastl, uofr)

    retorno1 = empsagres[0].retresultado1()
    retorno2 = empsagres[0].retornaIndice()
    retorno3 = empsagres[0].retresultado2()

    textoretorno = []
    textoretorno.append(empsagres[0])
    texto = pd.DataFrame(textoretorno)

    texto.to_csv("./static/datasets/cache_fila/" + str(numero) + ".csv")

    return retorno1, retorno2, retorno3


class UOFR:

    def __init__(self, chave):
        self.key = chave
        self.pagamentos = None

        self.pagamentosordem1 = None
        self.pagamentosordem2 = None
        self.indice = 0
        self.indice2 = 0
        self.valortotal_pago = 0

    def execute(self, df, dias1, chave):
        emp_rows = df[df["FONTE_REC"] + df["UNID_ORC"] == self.key]
        pagament = []
        indice = 0
        Dicionario = {}

        for _, row in emp_rows.iterrows():
            dtpag = row["DATA_PAGAMENTO"]
            dtliq = row["DATA_LIQ"]
            if not isinstance(dtliq, str):
                ab = "nulo"
            else:
                dttratada = datetime.strptime(dtpag, '%Y-%m-%d')
                dtliqtratada = datetime.strptime(dtliq, '%Y-%m-%d')

                chavedicio = str(dtpag)+'-'+str(dtliq)

                if (chavedicio not in Dicionario):
                    vetorinterno = [row["NUMERO_EMPENHO"], str(
                        row["CPF_CNPJ"]), row["VALOR_EMPENHO"], row["VALOR_PAGAMENTO"]]
                    Dicionario[chavedicio] = {"dtp": dttratada, "dtl": dtliqtratada,
                                              "quantidade": 1, "Pagamentosqultrapass": 0, "vetorzin": [vetorinterno]}

                else:
                    valoranterior = Dicionario[chavedicio]["quantidade"]
                    valoratual = valoranterior+1
                    Dicionario[chavedicio]["quantidade"] = valoratual

                    vetorinterno = [row["NUMERO_EMPENHO"], str(
                        row["CPF_CNPJ"]), row["VALOR_EMPENHO"], row["VALOR_PAGAMENTO"]]

                    vetor2 = Dicionario[chavedicio]["vetorzin"]
                    vetor2.append(vetorinterno)
                    Dicionario[chavedicio]["vetorzin"] = vetor2

        self.pagamentos = Dicionario
        self.indice = self.ordenaPagamentos(dias1)

    def ordenaPagamentos(self, ndias):
        Dicionario = self.pagamentos
        chavesordenadas = sorted(Dicionario.keys())
        quantidadetotaldesordem = 0  # quantidade de pagamentos q foram ultrapassados
        quantidadetotaldesordem2 = 0
        pontuacao = 0

        for i in range(1, len(chavesordenadas)):
            anteriores = chavesordenadas[0:i-1]
            datapagidx = Dicionario[chavesordenadas[i]]["dtp"]
            dataliqidx = Dicionario[chavesordenadas[i]]["dtl"]
            qtd = Dicionario[chavesordenadas[i]]["quantidade"]

            chavedicio = str(datapagidx)[:-9]+'-'+str(dataliqidx)[:-9]
            pontosporpagamento = 0

            dtl1 = Dicionario[chavesordenadas[i]]["dtl"]
            dtp1 = Dicionario[chavesordenadas[i]]["dtp"]

            varx = 0
            libera = 1
            for k in anteriores:
                dtl2 = Dicionario[k]["dtl"]
                dtp2 = Dicionario[k]["dtp"]

                if (datapagidx != Dicionario[k]["dtp"]) and (dtl2 > dtl1) and ((dtp1 - dtp2).days > ndias):
                    # Significa desresopeito a fila de pagamentos
                    dataantes = dtp2
                    diferencadias = dtp1 - dataantes
                    diff = diferencadias.days

                    # Antes do pagamento em questão
                    quantidadeantes = Dicionario[k]["quantidade"]
                    # QUantidade de pagamentos*(1+N)
                    pontosporpagamento += int(quantidadeantes) * \
                        int(qtd)*(1+int(diff/31))

                    varx += int(quantidadeantes)

                    if (libera == 1):
                        quantidadetotaldesordem += int(qtd)
                        quantidadetotaldesordem2 += int(quantidadeantes)
                    libera = 0

            Dicionario[chavedicio]["Pagamentosqultrapass"] = varx
            pontuacao += pontosporpagamento

        self.pagamentosordem1 = Dicionario
        aaa = [[k, v['dtp'], v['dtl'], v['quantidade'], v['Pagamentosqultrapass'],
                v['vetorzin']] for k, v in Dicionario.items()]
        bbb = [[k, v['dtp'], v['dtl'], v['quantidade'], v['Pagamentosqultrapass'],
                v['vetorzin']] for k, v in Dicionario.items()]
        self.pagamentosordem1 = aaa
        bbb.sort(reverse=True, key=pegaQtdultrapass)
        self.pagamentosordem2 = bbb

        return pontuacao

    def retcompare(self):  # PARA A COMPARAÇÃO
        return self.pagamentos

    def retresultado1(self):  # PARA A COMPARAÇÃO
        return self.pagamentosordem1

    def retresultado2(self):  # PARA A COMPARAÇÃO
        return self.pagamentosordem2

    def retornakey(self):
        return self.key

    def obterdados(self):
        return (self.numero_emp, self.fornecedor, self.cnpj, self.valor_emp)

    def obterdata(self):
        return self.data_empenho

    def retornafornec(self):
        return self.fornecedor

    def retornaIndice(self):
        return self.indice

    def __str__(self):
        return "UO+FONTE_{}\n ValorPago={} Indicetotal1={} \nPAGAMENTOS({}): {}\n".format(self.key, self.valortotal_pago, self.indice,  len(self.pagamentos), self.pagamentos)


def CriaDivisao(df, dias1, chave):
    uomaisfonte = []
    new_emp = UOFR(chave)
    new_emp.execute(df, dias1, chave)
    uomaisfonte.append(new_emp)

    return uomaisfonte


def CriaDivisao2(df, dias1):
    uofr_keys = (df["FONTE_REC"] + df["UNID_ORC"]).unique()
    uomaisfonte = []

    for i in uofr_keys:
        new_emp = UOFR(i)
        new_emp.execute(df, dias1, i)
        uomaisfonte.append(new_emp)

    return uomaisfonte


def calculaListaUOFR(df):
    return (df["FONTE_REC"] + df["UNID_ORC"]).unique()
