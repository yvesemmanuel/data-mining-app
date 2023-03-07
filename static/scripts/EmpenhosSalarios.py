from datetime import datetime

import pandas as pd

from . import MontaEmpenhosPorLinha as mtEmp
from . import Empenho as emp


empenhos = []


def montaEmpenhos(linhaPag, descr):
    format = '%Y-%m-%d'
    listaItems = linhaPag.split(';')
    nrEmpenho = listaItems[4]
    cnpj = listaItems[2]
    cpf = listaItems[3]
    descricao = descr
    nmFornecedor = listaItems[8]
    dtEmp = listaItems[5].split()
    dtEmpenho = datetime.strptime(dtEmp[0], format).date()
    datasEmpenhos = []
    valoresEmpenhos = []
    vlEmpenho = listaItems[1]

    if (float(listaItems[6]) < 40000):
        for i in range(9, len(listaItems)):
            if (listaItems[i] != '\n'):
                if (i % 2 != 0):
                    try:
                        res = bool(datetime.strptime(listaItems[i], format))
                        datasEmpenhos.append(listaItems[i])
                    except ValueError:

                        datasEmpenhos.append('2019-01-02')
                else:
                    if (listaItems[i].replace('.', '', 1).isdigit()):
                        valoresEmpenhos.append(float(listaItems[i]))
                    else:
                        valoresEmpenhos.append(float(667.5))

        empenhos.append(emp.Empenho(nrEmpenho, datasEmpenhos, valoresEmpenhos,
                        cpf, cnpj, vlEmpenho, 1, descricao, nmFornecedor))


sortedEmpenhos = []


def openFileEmpenhos(fileName):

    mtEmp.openFile(fileName)
    mtEmp.montaEmpenhos()
    linhasEmpenhos = mtEmp.getEmpenhos()

    import re
    s = re.split(r'[/;outputs;.]', fileName)
    ano = s[-4]
    mun = s[-3]
    file_desc = './static/datasets/outputs' + ano + '/desc_' + \
               mun + '.csv'
    df_desc = pd.read_csv(file_desc)

    for line in linhasEmpenhos[1:]:
        id_empenho = (line.split(";"))[4]
        d = df_desc.loc[df_desc['ID_EMPENHO'] == int(id_empenho)]["HISTORICO"].values[0]

        montaEmpenhos(line, d)

    emp = sorted(empenhos, key=lambda Empenho: Empenho.scoreRegularidade, reverse=False)

    import re
    s = re.split(r'[/;outputs;.]', fileName)
    ano = s[-4]
    mun = s[-3]
    path_desc = './static/datasets/outputs'+str(ano)+'/desc_'+str(mun)+'.csv'
    df_descr = pd.read_csv(path_desc)

    for e in emp:
        if (len(e.listDtPagamentos) >= 5):
            sortedEmpenhos.append(e)


def getSortedEmpenhos(fileName):
    global sortedEmpenhos
    global empenhos
    sortedEmpenhos = []
    empenhos = []
    openFileEmpenhos(fileName)

    return sortedEmpenhos
