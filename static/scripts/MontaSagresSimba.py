from . import SagresSimbaObj

dictSagres = {}
dictSimba = {}


def getSagresInfor(fileName):
    arquivo = ("./static/datasets/" + fileName)
    arq = open(arquivo, "r", encoding="utf8")
    linhasArquivoPagamento = arq.readlines()
    arq.close()

    for line in linhasArquivoPagamento:
        l = line.split(";")
        listPags = []
        for i in range(2, len(l)):
            listPags.append(l[i])
        dictSagres[str(l[0])+";"+str(l[1])] = listPags


def getSimbaInfor(fileName):
    arquivo = ("./static/datasets/" + fileName)
    arq = open(arquivo, "r", encoding="utf8")
    linhasArquivoPagamento = arq.readlines()
    arq.close()

    for line in linhasArquivoPagamento:
        l = line.split(";")
        listPags = []
        for i in range(1, len(l)):
            listPags.append(l[i])
        dictSimba[str(l[0])] = listPags


def montaObjsSagresSimba(fileNameSimba, fileNameSagres):
    getSagresInfor(fileNameSagres)
    getSimbaInfor(fileNameSimba)

    listSagresSimbaObjs = []

    for key in dictSagres:
        l = key.split(";")
        cpf_cnpj = str(l[0])
        nmFornecedor = l[1]
        listPagSagres = dictSagres.get(key)
        listPagSimba = dictSimba.get(cpf_cnpj)

        listSagresSimbaObjs.append(SagresSimbaObj.SagresSimbaObj(
            cpf_cnpj, nmFornecedor, listPagSimba, listPagSagres))

    sortedSagresSimbaObjs = sorted(listSagresSimbaObjs, key=lambda SagresSimbaObj: (
        SagresSimbaObj.somaSimba - SagresSimbaObj.somaSagres), reverse=True)

    return sortedSagresSimbaObjs
