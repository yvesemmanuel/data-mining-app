from datetime import datetime,timedelta
import static.scripts.MontaEmpenhosPorLinha as mtEmp
from static.scripts.Empenho import Empenho

empenhos = []

def montaEmpenhos(linhaPag):
    format = '%Y-%m-%d'
    listaItems = linhaPag.split(";")
    nrEmpenho = listaItems[4]
    cnpj = listaItems[2]
    cpf = listaItems[3]
    dtEmp = listaItems[5].split()
    dtEmpenho = datetime.strptime(dtEmp[0], '%Y-%m-%d').date()
    datasEmpenhos = []
    valoresEmpenhos = []
    vlEmp = listaItems[1]
    descricao = listaItems[7]
    nmFornecedor = listaItems[8]
    if((dtEmpenho > datetime.strptime("2019-01-01", '%Y-%m-%d').date()) and float(listaItems[6]) > 60000):
        for i in range(9,len(listaItems)):
            if(listaItems[i] != "\n"):
                if(i%2 != 0):
                    try:
                        res = bool(datetime.strptime(listaItems[i], format))
                        datasEmpenhos.append(listaItems[i])
                    except ValueError:
                        
                        datasEmpenhos.append('2019-01-02')
                else:
                    if(listaItems[i].replace('.','',1).isdigit()):
                        valoresEmpenhos.append(float(listaItems[i]))
                    else:
                        valoresEmpenhos.append(float(667.5))

        empenhos.append(Empenho(nrEmpenho,datasEmpenhos,valoresEmpenhos, cpf, cnpj, vlEmp, 0, descricao, nmFornecedor))


sortedEmpenhos = []
#Abre arquivo de empenhos
def openFileEmpenhos(fileName):


    mtEmp.openFile(fileName)
    mtEmp.montaEmpenhos()
    linhasEmpenhos = mtEmp.getEmpenhos()


    for line in linhasEmpenhos[1:]:
        montaEmpenhos(line)

    emp = sorted(empenhos, key=lambda Empenho: Empenho.scoreRegularidade)
    emp2 = []
    ct = 0
    for e in emp:
        # score = getScoreRegularidade(e.getDtPagamentosDatetime())
        if (len(e.listDtPagamentos) >= 5):
            #print(e.nrEmpenho, len(e.listDtPagamentos), ct, e.scoreRegularidade)
            sortedEmpenhos.append(e)
        ct = ct + 1

def getSortedEmpenhos(fileName):
    global sortedEmpenhos
    global empenhos
    sortedEmpenhos = []
    empenhos = []

    openFileEmpenhos(fileName)

    return sortedEmpenhos
