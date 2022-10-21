from flask import Flask, render_template, request
import pandas as pd
import json
from os import listdir
from static.scripts.UtilsUJsProcessadas import *
from static.scripts.MontaSagresSimba import *
from static.scripts.Getters import *
from static.scripts.Plots import *
from static.scripts.CreateMap import *
from static.scripts.AnaliseScoreUJS import *
from static.scripts.FilaP import *
import locale

locale.getlocale()
('pt_BR', 'UTF-8')

app = Flask(__name__)

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)
    

@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/analysis/regular_payments', methods=['GET', 'POST'])
def get_regular_payments():
    page_title = 'Análise de Pagamentos Regulares'
    city_options = list(
        pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';').Municipio
    )
    year_options = [2019, 2020]
    user_request = request.method

    if user_request == 'POST':
        city_selected = request.form.get('city')
        year_selected = request.form.get('year')
        supplier_selected = request.form.get('supplier', 0)
        action_selected = request.form.get('action')

        loans = get_salario_emp(city_selected, year_selected)
        supplier_options = []
        for idx, empenho in enumerate(loans):
            supplier_options.append(str(idx) + ' - ' + str(empenho.nmFornecedor))

        if action_selected == 'apply':
            loan_idx = 0
        elif action_selected == 'update':
            loan_idx = int(supplier_selected)

        loan_selected = loans[loan_idx]
        y = loan_selected.listValoresPagamentos
        x = loan_selected.datasPagamentosDateTime
        regular_payments_plot(x, y)

        supplier_id = '{} ({})'.format(loan_selected.cnpj, loan_selected.nmFornecedor)
        dates = '; '.join(map(date_to_string, loan_selected.datasPagamentosDateTime))
        values = '; '.join(map(str, loan_selected.listValoresPagamentos))
        description = loan_selected.descricao

        loan_info = {
            'CPF/CNPJ': supplier_id,
            'Datas': dates,
            'Valores': values,
            'Descrição': description,
        }

        return render_template(
            'pagamentos_regulares.html',
            page_title=page_title,
            city_options=city_options,
            year_options=year_options,
            user_request=user_request,
            
            supplier_options=supplier_options,
            loan_info=loan_info,
            city_selected=city_selected,
            year_selected=int(year_selected),
            year=int(year_selected),
            supplier_selected=int(supplier_selected),
        )

    return render_template(
        'pagamentos_regulares.html',
        page_title=page_title,
        city_options=city_options,
        year_options=year_options,
        user_request=user_request,
    )


@app.route('/analysis/servicos_antes_empenho', methods=['GET', 'POST'])
def servicos_antes():
    municipios = list(
        pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';').Municipio
    )

    anos = [2019, 2020]

    if request.method == 'POST':
        municipio = request.form.get('municipio')
        ano = request.form.get('ano')

        empenhos = get_servico_emp(municipio, ano)
        lista_empenhos = []
        for idx, empenho in enumerate(empenhos):
            lista_empenhos.append(str(idx) + ' - ' + str(empenho.nmFornecedor))

        if request.form.get('action') == 'aplicar':
            empenho = empenhos[0]
            criar_plot_2(empenho)
        elif request.form.get('action') == 'atualizar':
            num_empenho = int(request.form.get('empenho').split(' - ')[0])
            empenho = empenhos[num_empenho]
            criar_plot_2(empenho)

        cpf_cnpj = '{} ({})'.format(empenho.cnpj, empenho.nmFornecedor)
        primeiro_mes = str(round(empenho.vlMes1, 2))
        media_mensal = str(round(empenho.vlMedioMensal, 2))

        lista_datas = map(date_to_string, empenho.datasPagamentosDateTime)
        datas = '; '.join(lista_datas)

        lista_valores = map(str, empenho.listValoresPagamentos)
        valores = '; '.join(lista_valores)

        descricao = empenho.descricao

        info = {
            'cpf_cnpj': cpf_cnpj,
            'datas': datas,
            'valores': valores,
            'descricao': descricao,
            'primeiro_mes': primeiro_mes,
            'media_mensal': media_mensal,
        }

        return render_template(
            'servicos_antes.html',
            title='Análise de Serviços Antes de Empenho',
            municipios=municipios,
            method=request.method,
            anos=anos,
            ano_selecionado=ano,
            municipio_selecionado=municipio,
            empenho_selecionado=request.form.get('empenho'),
            lista_empenhos=lista_empenhos,
            info_empenho=info,
        )

    return render_template(
        'servicos_antes.html',
        title='Análise de Serviços Antes de Empenho',
        municipios=municipios,
        anos=anos,
        method=request.method,
    )


@app.route('/analysis/simba', methods=['GET', 'POST'])
def simba():
    lObjs = montaObjsSagresSimba(
        'simba/SimbaGoiana.csv', 'simba/SagresGoiana.csv')
    lst_idx_simba_sagres = []
    for idx, o in enumerate(lObjs):
        lst_idx_simba_sagres.append(
            '{} - {}({}) - {}'.format(
                idx, o.nmFornecedor, o.cpf_cnpj, round(
                    o.somaSimba - o.somaSagres, 2)
            )
        )

    meses = [
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez',
    ]

    if request.method == 'POST':
        entidade_idx = int(request.form.get('entidade').split(' - ')[0])
        entidade = lObjs[entidade_idx]

        dictPagsSagres = entidade.dictPagsMensaisSagres
        dictPagsSimba = entidade.dictPagsMensaisSimba

        linhaSagres = []
        linhaSimba = []

        for idx in range(1, 13):
            linhaSagres.append(round(dictPagsSagres[idx], 2))
            linhaSimba.append(round(dictPagsSimba[idx], 2))

        info = {'fornecedor': entidade.nmFornecedor}
        criar_plot_3(entidade_idx)

        tb_info = {'meses': meses, 'sagres': linhaSagres, 'simba': linhaSimba}

        return render_template(
            'simba.html',
            title='SIMBA',
            indexes=lst_idx_simba_sagres,
            info_entidade=info,
            table_info=tb_info,
            idx_selecionado=request.form.get('entidade'),
        )

    entidade_idx = 0
    entidade = lObjs[entidade_idx]

    dictPagsSagres = entidade.dictPagsMensaisSagres
    dictPagsSimba = entidade.dictPagsMensaisSimba

    linhaSagres = []
    linhaSimba = []

    for idx in range(1, 13):
        linhaSagres.append(round(dictPagsSagres[idx], 2))
        linhaSimba.append(round(dictPagsSimba[idx], 2))

    info = {'fornecedor': entidade.nmFornecedor}
    criar_plot_3(entidade_idx)

    tb_info = {'meses': meses, 'sagres': linhaSagres, 'simba': linhaSimba}

    return render_template(
        'simba.html',
        title='SIMBA',
        indexes=lst_idx_simba_sagres,
        info_entidade=info,
        table_info=tb_info,
        idx_selecionado=request.form.get('entidade'),
    )


@app.route('/analysis/atraso_pagamentos', methods=['GET', 'POST'])
def atraso_pagamentos():
    anos = [int(file.split('outputs')[1]) for file in listdir(
        './static/datasets') if 'outputs' in file]
    anos.sort()
    cores = ['Pior UO+FONTE', 'Média UO+FONTE']
    entidades = ['Pessoa Física', 'Pessoa Jurídica', 'Ambos']

    df_cidades = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')
    municipios = dict(zip(df_cidades.Municipio, df_cidades.numUJ))

    if request.method == 'POST':
        analise = request.form.get('analise')
        ano_selecionado = request.form.get('ano')
        cor_mapa = request.form.get('cormapa')
        municipio_selecionado = request.form.get('municipio')
        limite_atraso_selecionado = request.form.get('limite-dias')

        if analise == 'Análise de Atrasos':
            entidade_selecionada = request.form.get('entidade')
            limite_empenho = request.form.get('limite-empenho')
            limite_atraso = request.form.get('valor-limite', '0')

            for muni in municipios:
                if UJsProcessadas.getScoreUJ(muni, ano_selecionado, municipios[muni], float(limite_atraso), limite_empenho, entidade_selecionada, int(limite_atraso_selecionado), cor_mapa):
                    break

            caminhoDoDir = './static/datasets/cache_scores/'+ano_selecionado+'-'+limite_atraso + \
                '-'+limite_empenho+'-'+entidade_selecionada+'-'+limite_atraso_selecionado
            all_dfs = [pd.read_csv(caminhoDoDir + '/' + file)
                       for file in listdir(caminhoDoDir)]
            df_scores = pd.concat(all_dfs)
            df_scores.to_csv(caminhoDoDir+'/all_scores.csv', index=False)

            if request.form.get('consultar'):
                computaAtrasos(int(limite_atraso), int(ano_selecionado))

                listaUJSNaoFormatadas = resumoPorMunicipio[municipio_selecionado]['UJ']
                uj = request.form.get('empenho', listaUJSNaoFormatadas[0])
                
                df = getPagLiqsRes()
                criar_plot_4(df[df['UJ'] == uj])
                criar_plot_5(df[df['UJ'] == uj])

                return render_template(
                    'atraso_pagamentos.html',
                    title='Análise de Atraso de Pagamentos',
                    method=request.method,
                    anos=anos,
                    cores=cores,
                    entidades=entidades,
                    cor_selecionada=cor_mapa,
                    analise_selecionada=analise,
                    entidade_selecionada=entidade_selecionada,
                    limite_selecionado=limite_empenho,
                    empenho_selecionado=uj,
                    valor_selecionado=limite_atraso,
                    municipios=municipios,
                    ano_selecionado=ano_selecionado,
                    listaUJSNaoFormatadas=listaUJSNaoFormatadas,
                    municipio_selecionado=municipio_selecionado,
                    limite_atraso_selecionado=limite_atraso_selecionado,
                    plot_4=True,
                    plot_5=True
                )

            # criar_mapa_1(caminhoDoDir+'/all_scores.csv')

            return render_template(
                'atraso_pagamentos.html',
                title='Análise de Atraso de Pagamentos',
                method=request.method,
                anos=anos,
                cores=cores,
                entidades=entidades,
                cor_selecionada=cor_mapa,
                analise_selecionada=analise,
                entidade_selecionada=entidade_selecionada,
                limite_selecionado=limite_empenho,
                valor_selecionado=limite_atraso,
                ano_selecionado=int(ano_selecionado),
                municipios=municipios,
                limite_atraso_selecionado=limite_atraso_selecionado,
                plot_4=False,
                plot_5=False
            )
        elif analise == 'Análise de inconformidades':
            dados = pd.read_csv('./static/datasets/inconformidades/{}.csv'.format(ano_selecionado))
            dados = dados.drop(['qtd_liq_pag', 'uj', 'valor_liq'], axis=1)

            return render_template(
                'atraso_pagamentos.html',
                title='Análise de Atraso de Pagamentos',
                method=request.method,
                anos=anos,
                cores=cores,
                dados = dados,
                entidades=entidades,
                cor_selecionada=cor_mapa,
                analise_selecionada=analise,
                municipios=municipios,
                ano_selecionado=int(ano_selecionado),
                # municipio_selecionado=municipio_selecionado,
                limite_atraso_selecionado=limite_atraso_selecionado
            )

    return render_template(
        'atraso_pagamentos.html',
        title='Análise de Atraso de Pagamentos',
        anos=anos,
        method=request.method,
        cores=cores,
        entidades=entidades,
        municipios=municipios
    )


@app.route('/mapa_atrasos')
def mapa_atrasos():
    return render_template('mapa_atrasos.html')


@app.route('/plot')
def plot():
    return render_template('plot.html')


@app.route('/analysis/correspondencia_fontes', methods=['GET', 'POST'])
def correspondencia_fontes():
    df_cidades = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')
    municipios = dict(zip(df_cidades.Municipio, df_cidades.numUJ))

    if request.method == 'POST':
        municipio_selecionado = request.form.get('municipio')

        colunas, linhas, linhas_descricoes, descricao_geral = get_dados_correspondencia(
            municipio_selecionado)

        return render_template('correspondencia_fontes.html', title='Correspondência Entre Fontes de Dados', municipios=municipios, method=request.method, municipio_selecionado=municipio_selecionado, colunas=colunas, linhas=linhas, linhas_descricoes=json.dumps(linhas_descricoes), descricao_geral=descricao_geral)

    return render_template('correspondencia_fontes.html', title='Correspondência Entre Fontes de Dados', municipios=municipios, method=request.method)


def date_to_string(date):
    return date.strftime('%d/%m/%Y')


@app.route('/analysis/filas_pagamentos', methods=['GET', 'POST'])
def filas_pagamentos():
    df = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')
    municipios = df['Municipio'].tolist()
    dias_tolerancia = [7, 15, 30]
    colunas = ['Numero Empenho', 'CPF/CNPJ', 'VL Emp', 'VL Liq', 'Data Pag', 'Data Liq.', 'Qtd ultrapassaram']


    if request.method == 'POST':
        municipio = request.form.get('municipio', municipios[0])
        lista_fontes = get_lista_UOFR(municipio)
        fonte_selecionada = request.form.get('fonte', lista_fontes[0])
        num_municipio = int(df[df['Municipio'] == municipio].numUJ)

        if request.form.get('action') == 'aplicar':
            dias_selecionado = dias_tolerancia[0]
            result1, varia, _ = MudaMunicio(num_municipio, fonte_selecionada, int(dias_selecionado))

            return render_template('filas_pagamentos.html', municipios=municipios, municipio_selecionado=municipio,
                                    dias_tolerancia=dias_tolerancia, dias_selecionado=int(dias_selecionado), lista_fontes=lista_fontes, title='Filas de Pagamentos', pontuacao=varia, show_table=True, colunas=colunas, resultado=result1, fonte_selecionada=fonte_selecionada, method=request.method)
        else:
            dias_selecionado = request.form.get('dias')
            result1, varia, result2 = MudaMunicio(num_municipio, fonte_selecionada, int(dias_selecionado))

            return render_template('filas_pagamentos.html', municipios=municipios, municipio_selecionado=municipio,
                                    dias_tolerancia=dias_tolerancia, dias_selecionado=int(dias_selecionado), lista_fontes=lista_fontes, title='Filas de Pagamentos', pontuacao=varia, resultado=result1, fonte_selecionada=fonte_selecionada, show_table=True, colunas=colunas, method=request.method)

            

    return render_template('filas_pagamentos.html', municipios=municipios, dias_tolerancia=dias_tolerancia, title='Filas de Pagamentos', method=request.method)


@app.route('/mapa_filas')
def mapa_filas():
    criar_mapa_2()
    return render_template('mapa_filas.html')


if __name__ == '__main__':

    app.run(debug=True)
