import pandas as pd
from os import listdir
from os.path import isfile, join


#dfPagamentosLiq = pd.read_csv('/Users/georgegomescabral/PycharmProjects/CorrespSagresContab/outputs/5298.csv',  sep=",", index_col=False)

path = 'C:\\Users\\7063\PycharmProjects\\ordem_cronologica\\outputs2019\\'

files = [f for f in listdir(path) if isfile(join(path, f))]

dfAll = pd.read_csv('C:\\Users\\7063\PycharmProjects\\ordem_cronologica\\outputs2019\\5298.csv',  sep=",", index_col=False)

dfAll = pd.DataFrame(columns=dfAll.columns)

print(dfAll)

for file in files:

    if(str(file) != ".DS_Store"):
        print(path+str(file))
        df = pd.read_csv(path+str(file), sep=",",
                            index_col=False)
        dfAll = dfAll.append(df, ignore_index=True)

dfAll.to_csv(path+'allUJs.csv')

