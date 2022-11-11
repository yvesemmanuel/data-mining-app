from statistics import mean, stdev
from datetime import datetime


class Empenho:
    nrEmpenho = 0
    listDtPagamentos = []
    listValoresPagamentos = []
    datasPagamentosDateTime = []
    scoreRegularidade = 1000
    cpf = ''
    cnpj = ''
    nmFornecedor = ''
    vlEmpenho = 0
    descricao = ''
    vlMes1 = 0
    vlMedioMensal = 0

    def __init__(self, _nr_Emp, _datasPag, _valoresPag, _cpf, _cnpj, _vlEmpenho, _isSalario, _descricao, _nmFornecedor):
        self.listDtPagamentos = []
        self.listValoresPagamentos = []
        self.datasPagamentosDateTime = []
        self.scoreRegularidade = 1000
        self.vlEmpenho = _vlEmpenho
        self.cpf = _cpf
        self.cnpj = _cnpj
        self.nrEmpenho = _nr_Emp
        self.listDtPagamentos = _datasPag
        self.listValoresPagamentos = _valoresPag
        self.descricao = _descricao
        self.nmFornecedor = _nmFornecedor
        if (_isSalario == 1):
            self.getScoreRegularidadeSalario()
        else:
            self.getScoreRegularidadeAntecipacoesServicos()

    def getDtPagamentosDatetime(self):
        for i in self.listDtPagamentos:
            self.datasPagamentosDateTime.append(
                datetime.strptime(i, '%Y-%m-%d').date())
        return self.datasPagamentosDateTime

    def getScoreRegularidadeSalario(self):

        datasPagamentos = self.getDtPagamentosDatetime()
        listaSimilaridadesA30DiasIntervalo = []
        maisQueDoisPagamentos = False
        for idx in range(1, len(datasPagamentos)):
            diff = datasPagamentos[idx] - datasPagamentos[idx-1]
            listaSimilaridadesA30DiasIntervalo.append(abs(diff.days - 30))
            maisQueDoisPagamentos = True

        pagamentosNormalizados = self.listValoresPagamentos
        desvioPadrao = 0
        if (max(pagamentosNormalizados) != min(pagamentosNormalizados)):
            norm = [(float(i)-min(pagamentosNormalizados))/(max(pagamentosNormalizados) -
                                                            min(pagamentosNormalizados)) for i in pagamentosNormalizados]
            desvioPadrao = stdev(norm)

        if (maisQueDoisPagamentos):
            self.scoreRegularidade = mean(
                listaSimilaridadesA30DiasIntervalo) + desvioPadrao
        else:
            self.scoreRegularidade = 1000

    def getScoreRegularidadeAntecipacoesServicos(self):

        datasPagamentos = self.getDtPagamentosDatetime()
        listaSimilaridadesA30DiasIntervalo = []
        maisQueDoisPagamentos = False
        for idx in range(1, len(datasPagamentos)):
            diff = datasPagamentos[idx] - datasPagamentos[idx-1]
            listaSimilaridadesA30DiasIntervalo.append(abs(diff.days - 30))
            maisQueDoisPagamentos = True

        pagamentosNormalizados = self.listValoresPagamentos
        desvioPadrao = 0
        if (max(pagamentosNormalizados) != min(pagamentosNormalizados)):
            norm = [(float(i)-min(pagamentosNormalizados))/(max(pagamentosNormalizados) -
                                                            min(pagamentosNormalizados)) for i in pagamentosNormalizados]
            desvioPadrao = stdev(norm)

        dictPagsPorMes = {}
        for idx in range(len(datasPagamentos)):
            if datasPagamentos[idx].month not in dictPagsPorMes:
                dictPagsPorMes[datasPagamentos[idx].month] = self.listValoresPagamentos[idx]
            else:
                dictPagsPorMes[datasPagamentos[idx].month] += self.listValoresPagamentos[idx]

        keysList = list(dictPagsPorMes.keys())

        keysList = sorted(keysList)

        listPagsPorMes = []
        for l in keysList:
            listPagsPorMes.append(dictPagsPorMes[l])

        if (len(listPagsPorMes) > 2):
            mediaPags = mean(listPagsPorMes[1:-1])
            self.vlMedioMensal = mediaPags
            primeiroPagMensal = listPagsPorMes[0]
            self.vlMes1 = primeiroPagMensal
            percent = (primeiroPagMensal * 100) / mediaPags

            diffPercentual = (percent - 100) / 100
            # Printa diferença percentural, fornecedor e média para pagamentos por mês > 2
            #print(str(diffPercentual)+' '+self.nmFornecedor + ' '+ str(mediaPags))

            incrScore = 0
            if (stdev(self.listValoresPagamentos) == 0):
                incrScore = 100

            # esse score estah muito grosseiro, precisa de melhor preparacao
            #self.scoreRegularidade = mean(listaSimilaridadesA30DiasIntervalo)  - 5*diffPercentual
            self.scoreRegularidade = - diffPercentual + incrScore
        else:
            self.scoreRegularidade = 1000

    def getScoreRegularidadeServico(self):

        datasPagamentos = self.getDtPagamentosDatetime()
        listaSimilaridadesA30DiasIntervalo = []
        maisQueDoisPagamentos = False
        for idx in range(1, len(datasPagamentos)):
            diff = datasPagamentos[idx] - datasPagamentos[idx-1]
            listaSimilaridadesA30DiasIntervalo.append(abs(diff.days - 30))
            maisQueDoisPagamentos = True

        if (maisQueDoisPagamentos):
            self.scoreRegularidade = mean(listaSimilaridadesA30DiasIntervalo)
        else:
            self.scoreRegularidade = 1000
