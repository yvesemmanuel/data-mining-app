import pyodbc
import pandas as pd
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
cnxn = pyodbc.connect('Driver={SQL Server};Server=192.168.1.12;Trusted_Connection=yes;Database=Sagres2020;')

cursor = cnxn.cursor()

def getPagamentos(idxUJ):
    with open('querys/queryPagamentos.txt', 'r') as file:
        sql = file.read().replace('@idxuj', str(idxUJ))
        df = pd.read_sql(sql, cnxn)
        df['NOME_UO'] = pd.Series("", index=df.index)
        df['NOME_FONTE_REC'] = pd.Series("", index=df.index)
        df['PAG_E_RETENCAO'] = pd.Series(0, index=df.index)
        df['NUMERO_FONTERECURSOUG'] = pd.Series(0, index=df.index)
        df['NUMERO_DETALHAMENTO'] = pd.Series("-1", index=df.index)
        df['DATA_LIQ'] =  pd.to_datetime('2000-01-01', format='%Y-%m-%d')
        df['ID_EMPENHO'] = pd.to_numeric(df['ID_EMPENHO'])

        # soma pagamentos com retencoes
        for idx, i in df.iterrows():
            if (i['RETENCAO'] is not None):
                if(i['RETENCAO'] > 0):
                    df.loc[idx, "PAG_E_RETENCAO"] = i['VALOR'] + i['RETENCAO']
                else:
                    df.loc[idx, "PAG_E_RETENCAO"] = i['VALOR']
            else:
                df.loc[idx, "PAG_E_RETENCAO"] = i['VALOR']

        df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d')
        df['DATA_EMP'] = pd.to_datetime(df['DATA_EMP'], format='%Y-%m-%d')
        df['HOUVE_ESTORNO'] = 'n'

    df.to_csv("csv/"+str(idxUJ) + "_pag.csv")
    return df

def getEstornoPagamentos():
    with open('querys/queryEstornoPagamentos.txt', 'r') as file:
        sql = file.read()
        df = pd.read_sql(sql, cnxn)
        df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d')
        df['ID_EMPENHO'] = pd.to_numeric(df['ID_EMPENHO'])

    return df


def getLiquidacoes(idxUJ):
    with open('querys/queryLiquidacoes.txt', 'r') as file:
        sql = file.read().replace('@idxuj', str(idxUJ))
        df = pd.read_sql(sql, cnxn)
        df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d')
        df['ID_EMPENHO'] = pd.to_numeric(df['ID_EMPENHO'])
        df['FOI_PG'] = 0

    df.to_csv("csv/"+str(idxUJ) + "_liq.csv")
    return df

def getEstornoLiquidacoes():
    with open('querys/queryEstornoLiquidacoes.txt', 'r') as file:
        sql = file.read()
        df = pd.read_sql(sql, cnxn)
        df['ID_EMPENHO'] = pd.to_numeric(df['ID_EMPENHO'])
        df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d')

    return df


def getMunicipios():
    with open('querys/queryMunicipios.txt', 'r') as file:
        sql = file.read()
        df = pd.read_sql(sql, cnxn)

    return df

def getEmpenhosEstornados():
    with open('querys/queryEmpenhosEstornados.txt', 'r') as file:
        sql = file.read()
        df = pd.read_sql(sql, cnxn)
        df['DATA_EMPENHO'] = pd.to_datetime(df['DATA_EMPENHO'], format='%Y-%m-%d')
        df['ID_EMPENHO'] = pd.to_numeric(df['ID_EMPENHO'])

    df.to_csv("csv/empenhosEstornados.csv")
    return df