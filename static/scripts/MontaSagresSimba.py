from . import SagresSimbaObj


def get_sagres_info():
    sagres_info = {}
    file = open('./static/datasets/simba_sagres/SagresGoiana.csv', 'r', encoding='utf8')
    file_lines = file.readlines()
    file.close()

    for line in file_lines:
        l = line.split(';')
        listPags = []
        for i in range(2, len(l)):
            listPags.append(l[i])
        sagres_info[str(l[0])+';'+str(l[1])] = listPags

    return sagres_info


def get_simba_info():
    simba_info = {}
    arquivo = ('./static/datasets/simba_sagres/SimbaGoiana.csv')
    file = open(arquivo, 'r', encoding='utf8')
    file_lines = file.readlines()
    file.close()

    for line in file_lines:
        l = line.split(';')
        listPags = []
        for i in range(1, len(l)):
            listPags.append(l[i])
        simba_info[str(l[0])] = listPags

    return simba_info


def get_sagres_simba_objects():
    sagres_info = get_sagres_info()
    simba_info = get_simba_info()

    sagres_simba_objects = []
    for key in sagres_info:
        supplier_cpf_cnpj, supplier_name = key.split(';')

        sagres_payments = sagres_info.get(key)
        simba_payments = simba_info.get(supplier_cpf_cnpj)

        sagres_simba_objects.append(SagresSimbaObj.SagresSimbaObj(supplier_cpf_cnpj, supplier_name, simba_payments, sagres_payments))

    sort_key = lambda SagresSimbaObj: (SagresSimbaObj.somaSimba - SagresSimbaObj.somaSagres)
    sorted_sagres_simba_objects = sorted(sagres_simba_objects, key=sort_key, reverse=True)

    return sorted_sagres_simba_objects
