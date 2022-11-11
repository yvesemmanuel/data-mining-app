import pandas as pd
from datetime import datetime
import math


def pegaQtdultrapass(item):
    return item[4]


def MudaMunicipio2(index, numero, diastl, ano, tipop):
    muniselect = pd.read_csv(index, sep=',', usecols=['NUMERO_EMPENHO','DATA_EMP',
                                                      'VALOR_EMPENHO', 'DATA', 'CPF_CNPJ',
                                                      'DATA_LIQ', 'VALOR', 'FORNEC', 'ID_PAGAMENTO', 'NOME_FONTE_REC', 'NOME_UO'])

    camposuteismuni = muniselect
    camposuteismuni.rename(columns={'DATA': 'DATA_PAGAMENTO', "VALOR": "VALOR_PAGAMENTO",
                           'NOME_FONTE_REC': "FONTE_REC", 'NOME_UO': "UNID_ORC"},  inplace=True)

    vetorempsagres2 = CriaDivisao2(camposuteismuni, diastl, ano, tipop)
    calculo1 = 0
    for k in vetorempsagres2:
        calculo1 += k.retornaIndice()
    calculo1 = calculo1/len(vetorempsagres2)

    return calculo1


def MudaMunicio(numero, uofr, diastl, ano, tipop):
    if ano == '2020':
        muniselect = pd.read_csv("./static/datasets/pagamentos2020/" + str(numero) + ".csv", sep=',', usecols=['NUMERO_EMPENHO','DATA_EMP',
                                                                                                            'VALOR_EMPENHO', 'DATA', 'CPF_CNPJ',
                                                                                                            'DATA_LIQ', 'VALOR', 'FORNEC', 'ID_PAGAMENTO', 'NOME_FONTE_REC', 'NOME_UO'])
    else:
        muniselect = pd.read_csv("./static/datasets/pagamentos2019/" + str(numero) + ".csv", sep=',', usecols=['NUMERO_EMPENHO','DATA_EMP',
                                                                                                        'VALOR_EMPENHO', 'DATA', 'CPF_CNPJ',
                                                                                                        'DATA_LIQ', 'VALOR', 'FORNEC', 'ID_PAGAMENTO', 'NOME_FONTE_REC', 'NOME_UO'])


    camposuteismuni = muniselect
    camposuteismuni.rename(columns={'DATA': 'DATA_PAGAMENTO', "VALOR": "VALOR_PAGAMENTO",
                           'NOME_FONTE_REC': "FONTE_REC", 'NOME_UO': "UNID_ORC"},  inplace=True)

    empsagres = CriaDivisao(camposuteismuni, diastl, uofr, ano, tipop)


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
        self.listachavesdtframefiltrado = []

    def execute(self, df, dias1, chave, ano, tipop):

        valorlicitacao = 17600

        emp_rows = df[df["FONTE_REC"] + df["UNID_ORC"] == self.key]
        emp_rows1 = []
        chavesfiltradas = []
        if tipop == 'Dispensa':
            if ano == '2020':
                emp_rows1 = emp_rows[emp_rows.eval("DATA_EMP > '2020-03-19' & VALOR_EMPENHO <= 50000 | DATA_EMP <= '2020-03-19' & VALOR_EMPENHO <= 17600 ")]
            else:
                emp_rows1 = emp_rows[emp_rows["VALOR_EMPENHO"] <= 17600]
        elif tipop == 'Licitação':
            if ano == '2020':
                emp_rows1 = emp_rows[emp_rows.eval("DATA_EMP > '2020-03-19' & VALOR_EMPENHO > 50000 | DATA_EMP <= '2020-03-19' & VALOR_EMPENHO > 17600 ")]
            else:
                emp_rows1 = emp_rows[emp_rows["VALOR_EMPENHO"] > 17600]

        if(len(emp_rows1) > 0):
            chavesfiltradas = (emp_rows1["DATA_PAGAMENTO"] + emp_rows1["DATA_LIQ"]).unique()
            for i,v in enumerate(chavesfiltradas):
                part1 = v[:10]
                part2 = v[10:]
                final_string = part1 + '-' + part2
                chavesfiltradas[i] = final_string

        #print(chavesfiltradas)
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

                    if chavedicio in chavesfiltradas:
                        pertenceaofiltro = 1
                    else:
                        pertenceaofiltro = 0
                    vetorinterno = [row["NUMERO_EMPENHO"], str(
                        row["CPF_CNPJ"]), row["VALOR_EMPENHO"], row["VALOR_PAGAMENTO"]]
                    Dicionario[chavedicio] = {"dtp": dttratada, "dtl": dtliqtratada,
                                              "quantidade": 1, "Pagamentosqultrapass": 0, "ehfiltrado": pertenceaofiltro, "vetorzin": [vetorinterno]}

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
        self.listachavesdtframefiltrado = chavesfiltradas
        self.indice = self.ordenaPagamentos(dias1)
        

    def ordenaPagamentos(self, ndias):
        Dicionario = self.pagamentos
        chavesordenadas = sorted(Dicionario.keys())
        #print(chavesordenadas)
        quantidadetotaldesordem = 0  # quantidade de pagamentos q foram ultrapassados
        quantidadetotaldesordem2 = 0
        pontuacao = 0

        ehfiltrado = False
        listafiltrada = []
        if len(self.listachavesdtframefiltrado) > 0:
            ehfiltrado = True
            listafiltrada = self.listachavesdtframefiltrado
        

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

            if(ehfiltrado == False) or (ehfiltrado == True and chavedicio in listafiltrada):
                if(datapagidx-dataliqidx).days > ndias:
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

                            #3 * 8
                            peso = math.log(1+int(diff/31),2.1)
                            # QUantidade de pagamentos*(1+N)
                            pontosporpagamento += int(quantidadeantes) * \
                                int(qtd)*1
                                #int(qtd)*(1+int(diff/31))

                            varx += int(quantidadeantes)

                            if (libera == 1):
                                quantidadetotaldesordem += int(qtd)
                                quantidadetotaldesordem2 += int(quantidadeantes)
                            libera = 0

                    Dicionario[chavedicio]["Pagamentosqultrapass"] = varx
                    pontuacao += pontosporpagamento

        #self.pagamentosordem1 = Dicionario
        if ehfiltrado:
            tabelafinal = [[k, v['dtp'], v['dtl'], v['quantidade'], v['Pagamentosqultrapass'],
                    v['vetorzin']] for k, v in Dicionario.items() if v['ehfiltrado'] == 1]
        else:
            tabelafinal = [[k, v['dtp'], v['dtl'], v['quantidade'], v['Pagamentosqultrapass'],
                    v['vetorzin']] for k, v in Dicionario.items()]
        #bbb = [[k, v['dtp'], v['dtl'], v['quantidade'], v['Pagamentosqultrapass'],
        #        v['vetorzin']] for k, v in Dicionario.items()]
        self.pagamentosordem1 = tabelafinal
        #bbb.sort(reverse=True, key=pegaQtdultrapass)
        self.pagamentosordem2 = []

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


def CriaDivisao(df, dias1, chave, ano, tipop):
    uomaisfonte = []
    new_emp = UOFR(chave)
    new_emp.execute(df, dias1, chave, ano, tipop)
    uomaisfonte.append(new_emp)

    print(uomaisfonte)

    return uomaisfonte


def CriaDivisao2(df, dias1, ano, tipop):
    uofr_keys = (df["FONTE_REC"] + df["UNID_ORC"]).unique()
    uomaisfonte = []

    for i in uofr_keys:
        new_emp = UOFR(i)
        new_emp.execute(df, dias1, i, ano, tipop)
        uomaisfonte.append(new_emp)

    return uomaisfonte


def calculaListaUOFR(df):
    return (df["FONTE_REC"] + df["UNID_ORC"]).unique()
