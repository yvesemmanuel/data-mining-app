##Cabeçalho:
##Nr_Empenho;DataEmisEmp;ValorEmpenhado;Data_Liq;ValorSE;DataPgmtSE;INSMF

from datetime import datetime
import pandas as pd

linhasArquivoPagamento = []


def openFile(fileName):
    global linhasArquivoPagamento

    arquivo = (fileName)
    dados = []
    with open(arquivo, 'r') as file:
        data = file.readlines()
        #print(data)
        for i in data:
            dados.append(i.replace(", ", " "))
        #print(dados[0])

    array = list(dados)
    variavel1 = pd.DataFrame(array)
    variavel2 = variavel1[0].str.split(",").replace("\n", "")
    
    colunas = variavel2[0] 

    variavel4 = pd.DataFrame(variavel2[1:-1].to_list())
    tamcolunas = len(variavel4.loc[0,:])
    # print(tamcolunas)
    adicionar = list(range(tamcolunas-len(colunas)))
    #print(map(str, adicionar))
    colunas=colunas + adicionar
    variavel4.columns=colunas


    variavel3 = variavel4.loc[:,['ID_EMPENHO','NUMERO_EMPENHO','VALOR_EMPENHO','DATA_LIQ','PAG_E_RETENCAO','FORNEC','CPF_CNPJ','VALOR','DATA']]

    linhasArquivoPagamento = variavel3

empenhos = []

def montaEmpenhos():
    global linhasArquivoPagamento
    global empenhos
    empenhos = []

    colunas = 0
    max_colunas = 0
    max_colunas2 = 0

    parcelas = []
    cpf_cnpj = ""
    id_empenho = 0
    data_empenho = ""
    valor_empenho = ""
    descricao = "descricao"
    empenho = ""

    myDict = {}

    #Criar nova Estrutura (dicionário), para juntar pagamentos de mesmo id

    for index,linha in linhasArquivoPagamento.iterrows():
        
        if linha['ID_EMPENHO'] != id_empenho:

            if colunas > max_colunas:
                max_colunas = colunas
            if colunas > max_colunas2:
                max_colunas2 = colunas

            if (id_empenho != 0):

                idemptemp = str(id_empenho)
                parc = str(round(sum(parcelas), 2))
                if str(id_empenho) not in myDict:
                    
                    
                    valores = {"col": colunas, "parcelas": parc, "cpf_cnpj": cpf_cnpj, "datae": data_empenho, 
                    "valore": valor_empenho, "descricaoe": descricao, "fornec": fornecedor, "empenho": empenho}
                    myDict[idemptemp] = valores
                
                elif str(id_empenho) in myDict:
                    myDict[idemptemp]["empenho"] = myDict[idemptemp]["empenho"] + empenho
                    colunasint = myDict[idemptemp]["col"]
                    myDict[idemptemp]["col"] = colunasint + colunas
                    colunasint += colunas

                    if colunasint > max_colunas:
                        max_colunas2 = colunas


                #estruturadict = {"id": "", "valores"}
                '''empenhos.append(
                    str(colunas) + ";" + parc + ";" + cpf_cnpj + ";" + cpf_cnpj + ";" + str(
                        id_empenho) + ";" + data_empenho + ";" + valor_empenho + ";"
                    + descricao + ";"+ fornecedor +";"+ empenho + "\n")'''
                # print(str(colunas) + ";" + str(round(sum(parcelas), 2)) + ";" + cpf_cnpj + ";" + cpf_cnpj + ";" + str(
                #         id_empenho) + ";" + data_empenho + ";" + valor_empenho + ";"
                #     + descricao + ";" + empenho + "\n")
            else:
                #Não entra aqui, a nao ser q seja id = 0
                empenhos.append("cabecalho")

            colunas = 1

            parcelas = []
            data_pagamento = []

            cpf_cnpj = str(linha['CPF_CNPJ'])
            id_empenho = linha['ID_EMPENHO']
            data_empenho = "2019-04-05" #Data qualquer
            valor_empenho = str(linha['VALOR_EMPENHO'])
            valordopag = linha['VALOR']
            parcelas.append(float(valordopag))
            fornecedor = linha['FORNEC']
            descricao = "Sem descricao no momento" #Não possui na base
            dataPg = linha['DATA']
            data_pagamento.append(datetime.strptime(dataPg, '%Y-%m-%d').date())
            empenho = dataPg + ";" + str(valordopag) + ";"
        else:
            colunas += 1
            valordopag = linha['VALOR']
            parcelas.append(float(valordopag))
            dataPg = linha['DATA']
            data_pagamento.append(datetime.strptime(dataPg, '%Y-%m-%d').date())
            empenho += dataPg + ";" + str(valordopag) + ";"


    if colunas > max_colunas:
        max_colunas = colunas
    if colunas > max_colunas2:
        max_colunas2 = colunas


    idemptemp = str(id_empenho)
    parc = str(round(sum(parcelas), 2))
    if str(id_empenho) not in myDict:           
        valores = {"col": colunas, "parcelas": parc, "cpf_cnpj": cpf_cnpj, "datae": data_empenho, 
        "valore": valor_empenho, "descricaoe": descricao, "fornec": fornecedor, "empenho": empenho}
        myDict[idemptemp] = valores            
    elif str(id_empenho) in myDict:
        myDict[idemptemp]["empenho"] = myDict[idemptemp]["empenho"] + empenho
        colunasint = myDict[idemptemp]["col"]
        myDict[idemptemp]["col"] = colunasint + colunas
        colunasint += colunas

        if colunasint > max_colunas:
            max_colunas2 = colunas
    

    for key, value in myDict.items():
        vcol = str(value["col"])
        vparc = value["parcelas"]
        vcpf = value["cpf_cnpj"]
        vdata = value["datae"]
        vvalor = value["valore"]
        vdesc = value["descricaoe"]
        vfornec = value["fornec"]
        vemp = value["empenho"]
        empenhos.append(vcol + ";" + vparc + ";" + vcpf + ";" + vcpf + ";" + str(key) + ";" 
        + vdata + ";" + vvalor + ";" + vdesc + ";" + vfornec + ";" + vemp + "\n")
    '''empenhos.append(str(colunas) + ";" + parc + ";" + cpf_cnpj + ";" + cpf_cnpj + ";" + str(
            id_empenho) + ";" + data_empenho + ";" + valor_empenho + ";"
                        + descricao + ";"
                        + fornecedor + ";" + empenho + "\n")'''

    


    #CABEÇALHO P/ MAXIMO DE COLUNAS
    cabecalho = "QUANTIDADE_PARCELAS;SOMA_PARCELAS;CPF/CNPJ;CPF/CNPJ;ID_EMPENHO;DATA_EMPENHO;VALOR_TOTAL_EMPENHO;DESCRICAO;"
    for i in range(max_colunas2):
        cabecalho += "DATA_PAGAMENTO_" + str(i + 1) + ";"
        cabecalho += "VALOR_SUB_EMPENHO_" + str(i + 1) + ";"

    empenhos[0] = cabecalho + "\n"

    arquivo = ("./static/datasets/resultado222.csv")
    arq = open(arquivo, 'w', encoding="utf8")
    arq.writelines(empenhos)
    arq.close()
    linhasArquivoPagamento = []

def getEmpenhos():
    global empenhos
    return empenhos

