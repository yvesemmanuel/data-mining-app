class SagresSimbaObj:
    nmFornecedor = ""
    cpf_cnpj = ""
    somaSimba = 0
    somaSagres = 0
    listaPagsSimba = []
    listaPagsSagres = []
    dictPagsMensaisSagres = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    dictPagsMensaisSimba = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}


    def __init__(self, _cpf_cnpj, _nmFornecedor, _listaSimba, _listaSagres):

        self.cpf_cnpj = _cpf_cnpj
        self.nmFornecedor = _nmFornecedor
        self.listaPagsSimba = _listaSimba
        self.listaPagsSagres = _listaSagres

        dictSimba = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        dictSagres = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

        for s in self.listaPagsSagres:
            if(s != "\n"):
                l = s.split(",")
                vl = float(l[0])
                listaDt = str(l[1]).split("-")
                mes = int(listaDt[1])
                dictSagres[mes] += vl
                self.somaSagres += vl

        for s in self.listaPagsSimba:
            if (s != "\n"):
                l = s.split(",")
                vl = float(l[0])
                listaDt = str(l[1]).split("-")
                mes = int(listaDt[1])
                dictSimba[mes] += vl
                self.somaSimba += vl

        self.dictPagsMensaisSagres = dictSagres
        self.dictPagsMensaisSimba = dictSimba