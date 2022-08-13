from static.scripts.SagresSimbaObj import *




dictSagres = {}
dictSimba = {}

def getSagresInfor(fileName):
    global dictSagres

    arquivo = ("./static/datasets/" + fileName)
    arq = open(arquivo, 'r', encoding="utf8")
    linhasArquivoPagamento = arq.readlines()
    arq.close()

    for line in linhasArquivoPagamento:
        l = line.split(";")
        listPags = []
        for i in range(2,len(l)):
            listPags.append(l[i])
        dictSagres[str(l[0])+";"+str(l[1])] = listPags


def getSimbaInfor(fileName):
    global dictSimba

    arquivo = ("./static/datasets/" + fileName)
    arq = open(arquivo, 'r', encoding="utf8")
    linhasArquivoPagamento = arq.readlines()
    arq.close()

    for line in linhasArquivoPagamento:
        l = line.split(";")
        listPags = []
        for i in range(1,len(l)):
            listPags.append(l[i])
        dictSimba[str(l[0])] = listPags

def montaObjsSagresSimba(fileNameSimba, fileNameSagres):
    global dictSagres
    global dictSimba

    getSagresInfor(fileNameSagres)
    getSimbaInfor(fileNameSimba)

    listSagresSimbaObjs = []

    for key in dictSagres:
        l = key.split(";")
        cpf_cnpj = str(l[0])
        nmFornecedor = l[1]
        listPagSagres = dictSagres.get(key)
        listPagSimba = dictSimba.get(cpf_cnpj)

        listSagresSimbaObjs.append(SagresSimbaObj(cpf_cnpj, nmFornecedor, listPagSimba, listPagSagres))

    sortedSagresSimbaObjs = sorted(listSagresSimbaObjs, key=lambda SagresSimbaObj: (SagresSimbaObj.somaSimba - SagresSimbaObj.somaSagres), reverse = True)

    return sortedSagresSimbaObjs


montaObjsSagresSimba("simba/SimbaGoiana.csv", "simba/SagresGoiana.csv")
