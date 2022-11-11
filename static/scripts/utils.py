

def date_to_string(date):
    return date.strftime('%d/%m/%Y')


def format_cnpj_cpf(x):
    cnpj_filled = str(int(x)).zfill(14)

    if cnpj_filled[8:12] not in ['0001', '0002']:
        cpf_filled = str(int(x)).zfill(11)        
        return '{}.{}.{}-{}'.format(cpf_filled[:3], cpf_filled[3:6], cpf_filled[6:9], cpf_filled[9:11])
    
    return '{}.{}.{}/{}-{}'.format(cnpj_filled[:2], cnpj_filled[2:5], cnpj_filled[5:8], cnpj_filled[8:12], cnpj_filled[12:])