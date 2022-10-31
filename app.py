from turtle import update
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
def regular_payments():
    page_title = 'Análise de Pagamentos Regulares'
    city_options = list(
        pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';').Municipio
    )
    year_options = [2019, 2020]
    user_request = request.method

    if user_request == 'POST':
        selected_city = request.form.get('city')
        selected_year = request.form.get('year')
        selected_supplier = request.form.get('supplier', 0)
        selected_action = request.form.get('action')

        loans = get_salario_emp(selected_city, selected_year)
        supplier_options = []
        for idx, empenho in enumerate(loans):
            supplier_options.append(
                str(idx) + ' - ' + str(empenho.nmFornecedor))

        if selected_action == 'apply':
            loan_idx = 0
        elif selected_action == 'update':
            loan_idx = int(selected_supplier)

        loan_selected = loans[loan_idx]
        y = loan_selected.listValoresPagamentos
        x = loan_selected.datasPagamentosDateTime
        regular_payments_plot(x, y)

        supplier_id = '{} ({})'.format(
            loan_selected.cnpj, loan_selected.nmFornecedor)
        dates = '; '.join(
            map(date_to_string, loan_selected.datasPagamentosDateTime))
        values = '; '.join(map(str, loan_selected.listValoresPagamentos))
        description = loan_selected.descricao

        loan_info = {
            'CPF/CNPJ': supplier_id,
            'Datas': dates,
            'Valores': values,
            'Descrição': description,
        }

        return render_template(
            'payments_regular.html',
            page_title=page_title,
            city_options=city_options,
            year_options=year_options,
            user_request=user_request,

            supplier_options=supplier_options,
            loan_info=loan_info,
            selected_city=selected_city,
            selected_year=int(selected_year),
            selected_supplier=int(selected_supplier),
        )

    return render_template(
        'payments_regular.html',
        page_title=page_title,
        city_options=city_options,
        year_options=year_options,
        user_request=user_request,
    )


@app.route('/analysis/service_before_payment', methods=['GET', 'POST'])
def service_before_payment():
    page_title = 'Análise de Serviços Antes de Empenho'
    city_options = list(
        pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';').Municipio
    )
    year_options = [2019, 2020]
    user_request = request.method

    if user_request == 'POST':
        selected_city = request.form.get('city')
        selected_year = request.form.get('year')
        selected_supplier = request.form.get('supplier', 0)
        selected_action = request.form.get('action')

        loans = get_servico_emp(selected_city, selected_year)
        supplier_options = []
        for idx, loan in enumerate(loans):
            supplier_options.append(str(idx) + ' - ' + str(loan.nmFornecedor))

        if selected_action == 'apply':
            loan_idx = 0
        elif selected_action == 'update':
            loan_idx = int(selected_supplier)

        loan_selected = loans[loan_idx]
        y = loan_selected.listValoresPagamentos
        x = loan_selected.datasPagamentosDateTime
        service_before_payment_plot(x, y)

        supplier_id = '{} ({})'.format(
            loan_selected.cnpj, loan_selected.nmFornecedor)
        dates = '; '.join(
            map(date_to_string, loan_selected.datasPagamentosDateTime))
        values = '; '.join(map(str, loan_selected.listValoresPagamentos))
        description = loan_selected.descricao
        first_month = str(round(loan_selected.vlMes1, 2))
        monthly_average = str(round(loan_selected.vlMedioMensal, 2))

        loan_info = {
            'CPF/CNPJ': supplier_id,
            'Datas': dates,
            'Valores': values,
            'Descrição': description,
            'Primeiro Mês': first_month,
            'Média Mensal': monthly_average
        }

        return render_template(
            'service_before_payment.html',
            page_title=page_title,
            city_options=city_options,
            year_options=year_options,
            user_request=user_request,

            supplier_options=supplier_options,
            loan_info=loan_info,
            selected_city=selected_city,
            selected_year=int(selected_year),
            year=int(selected_year),
            selected_supplier=int(selected_supplier),
        )

    return render_template(
        'service_before_payment.html',
        page_title=page_title,
        city_options=city_options,
        year_options=year_options,
        user_request=user_request,
    )


@app.route('/analysis/simba', methods=['GET', 'POST'])
def simba():
    page_title = 'SIMBA'
    lObjs = montaObjsSagresSimba(
        'simba/SimbaGoiana.csv', 'simba/SagresGoiana.csv')
    entity_options = []
    for idx, o in enumerate(lObjs):
        entity_options.append(
            '{} - {}({}) - {}'.format(
                idx, o.nmFornecedor, o.cpf_cnpj, round(
                    o.somaSimba - o.somaSagres, 2)
            )
        )

    selected_entity = int(request.form.get('entity', 0))

    entity = lObjs[selected_entity]
    simba_plot(selected_entity)

    dictPagsSagres = entity.dictPagsMensaisSagres
    dictPagsSimba = entity.dictPagsMensaisSimba
    linhaSagres = []
    linhaSimba = []
    for idx in range(1, 13):
        linhaSagres.append(round(dictPagsSagres[idx], 2))
        linhaSimba.append(round(dictPagsSimba[idx], 2))

    entity_info = {'months': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul',
                              'Ago', 'Set', 'Out', 'Nov', 'Dez'], 'sagres': linhaSagres, 'simba': linhaSimba}

    return render_template(
        'simba.html',
        # rendering
        page_title=page_title,
        # input
        selected_entity=selected_entity,
        # output
        entity_info=entity_info,
        entity_options=entity_options,
    )


@app.route('/analysis/payments_delay', methods=['GET', 'POST'])
def payments_delay():
    page_title = 'Análise de Atraso de Pagamentos'
    city_df = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')
    city_options = dict(zip(city_df.Municipio, city_df.numUJ))
    year_options = [int(file.split('outputs')[1]) for file in listdir(
        './static/datasets') if 'outputs' in file]
    year_options.sort()
    map_options = ['Pior UO+FONTE', 'Média UO+FONTE']
    entity_options = ['Pessoa Física', 'Pessoa Jurídica', 'Ambos']
    user_request = request.method

    if user_request == 'POST':
        selected_analysis = request.form.get('analysis')
        selected_year = request.form.get('year')
        selected_map = request.form.get('map')
        selected_city = request.form.get('city')
        days_limit_selected = request.form.get('days-limit')

        if selected_analysis == 'Análise de Atrasos':
            selected_entity = request.form.get('entity')
            selected_loan_limit = request.form.get('loan-limit')
            loan_value_limit = request.form.get('loan-value', '0')

            for selected_city in city_options:
                if UJsProcessadas.getScoreUJ(selected_city, selected_year, city_options[selected_city], float(loan_value_limit), selected_loan_limit, selected_entity, int(days_limit_selected), selected_map):
                    break

            filepath = './static/datasets/cache_scores/'+selected_year+'-'+loan_value_limit + \
                '-'+selected_loan_limit+'-'+selected_entity+'-'+days_limit_selected
            all_dfs = [pd.read_csv(filepath + '/' + file)
                       for file in listdir(filepath)]
            df_smap_options = pd.concat(all_dfs)
            df_smap_options.to_csv(
                filepath+'/all_smap_options.csv', index=False)

            if request.form.get('consult'):
                computaAtrasos(int(loan_value_limit), int(selected_year))

                loans = resumoPorMunicipio[selected_city]['UJ']
                selected_loan = request.form.get(
                    'loan', loans[0])

                df = getPagLiqsRes()
                plots_df = df[df['UJ'] == selected_loan]

                x = plots_df["DIFF_LIQ_PAG"]
                y = plots_df["VALOR"]

                payments_delay_plot_0(x, y)
                payments_delay_plot_1(plots_df)

                return render_template(
                    'payments_delay.html',
                    # rendering
                    page_title=page_title,
                    city_options=city_options,
                    year_options=year_options,
                    map_options=map_options,
                    entity_options=entity_options,
                    user_request=user_request,

                    # input
                    selected_entity=selected_entity,
                    selected_loan_limit=selected_loan_limit,
                    selected_map=selected_map,
                    selected_analysis=selected_analysis,
                    selected_loan=selected_loan,
                    selected_year=selected_year,
                    selected_city=selected_city,
                    loan_value_limit=loan_value_limit,

                    # output
                    loans=loans,
                    days_limit_selected=days_limit_selected,
                    plot_0=True,
                    plot_1=True
                )

            payments_delay_map(filepath+'/all_smap_options.csv')

            return render_template(
                'payments_delay.html',
                # rendering
                page_title=page_title,
                city_options=city_options,
                year_options=year_options,
                map_options=map_options,
                entity_options=entity_options,
                user_request=user_request,
                selected_year=int(selected_year),
                selected_map=selected_map,

                selected_entity=selected_entity,
                selected_loan_limit=selected_loan_limit,
                selected_analysis=selected_analysis,
                loan_value_limit=loan_value_limit,
                days_limit_selected=days_limit_selected,
                plot_0=False,
                plot_1=False
            )
        elif selected_analysis == 'Análise de inconformidades':
            table_df = pd.read_csv(
                './static/datasets/inconformidades/{}.csv'.format(selected_year))
            table_df = table_df.drop(
                ['qtd_liq_pag', 'uj', 'valor_liq'], axis=1)

            return render_template(
                'payments_delay.html',
                page_title=page_title,
                city_options=city_options,
                year_options=year_options,
                map_options=map_options,
                entity_options=entity_options,
                user_request=user_request,

                selected_year=int(selected_year),
                table_df=table_df,
                selected_map=selected_map,
                selected_analysis=selected_analysis,
                days_limit_selected=days_limit_selected
                # selected_city=selected_city,
            )

    return render_template(
        'payments_delay.html',
        # rendering
        page_title=page_title,
        city_options=city_options,
        year_options=year_options,
        map_options=map_options,
        entity_options=entity_options,
        user_request=user_request
    )


@app.route('/payments_delay_map')
def payments_delay_map():
    return render_template('payments_delay_map.html')


@app.route('/payments_delay_plot_1')
def payments_delay_plot_1():
    return render_template('payments_delay_plot_1.html')


@app.route('/analysis/matching_sources', methods=['GET', 'POST'])
def matching_sources():
    page_title = 'Correspondência Entre Fontes de Dados'
    # df_cities = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')
    # city_options = dict(zip(df_cities.Municipio, df_cities.numUJ))
    city_options = ['Cabo de Santo Agostinho']
    user_request = request.method

    if user_request == 'POST':
        selected_city = request.form.get('city')

        columns, rows, payment_rows, row_general_descriptions, columns_general_descriptions = get_dados_correspondencia(
            selected_city)

        return render_template(
            'matching_sources.html',
            # rendering
            page_title=page_title,
            city_options=city_options,
            user_request=user_request,

            # input
            selected_city=selected_city,

            # output
            columns=columns,
            rows=rows,
            payment_rows=json.dumps(payment_rows),
            row_general_descriptions=row_general_descriptions,
            columns_general_descriptions=columns_general_descriptions
        )

    return render_template('matching_sources.html',
                            # rendering
                            page_title=page_title,
                            city_options=city_options,
                            user_request=user_request)


def date_to_string(date):
    return date.strftime('%d/%m/%Y')


@app.route('/analysis/payments_queue', methods=['GET', 'POST'])
def payments_queue():
    page_title = 'Filas de Pagamentos'
    df = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')
    city_options = df['Municipio'].tolist()

    year_options = ['2019','2020']
    payment_types = ['Geral','Dispensa','Licitação']

    days_of_tolerance = [7, 30, 60]
    columns = ['Numero Empenho', 'CPF/CNPJ', 'VL Emp',
               'VL Liq', 'Data Pag', 'Data Liq.', 'Qtd ultrapassaram']          
    user_request = request.method
    selected_action = request.form.get('action')
    selected_year = request.form.get('year', year_options[0])
    selected_day = days_of_tolerance[0]
    sources = get_lista_UOFR(city_options[0], '2019')

    if user_request == 'POST':
        print("Chegou aquiiii")
        selected_city = request.form.get('city', city_options[0])
        selected_year = request.form.get('year', year_options[0])
        
        selected_action = request.form.get('action')
        
        if (selected_action == 'update2' or selected_action != 'apply') or selected_action != 'update':
            sources = get_lista_UOFR(selected_city, selected_year)
        selected_source = request.form.get('source', sources[0])

        selected_payment = request.form.get('payment', payment_types[0])
        cities_num = int(df[df['Municipio'] == selected_city].numUJ)
        

        if selected_action == 'apply' or selected_action == 'update':
            selected_day = request.form.get('day', int(7))

            tipopagamento = request.form.get('payment', payment_types[0])

            rows, varia, _ = MudaMunicio(
            cities_num, selected_source, int(selected_day), selected_year, tipopagamento)

            return render_template('payments_queue.html',
                                    acao = selected_action,
                                    # rendering
                                    page_title=page_title,
                                    city_options=city_options,
                                    year_options=year_options,
                                    days_of_tolerance=days_of_tolerance,
                                    user_request=user_request,
                                    payment_types=payment_types,
                                    
                                    # input
                                    selected_city=selected_city,
                                    selected_year=selected_year,
                                    selected_day=int(selected_day),
                                    selected_source=selected_source,
                                    selected_payment=selected_payment,
                                    

                                    # output
                                    sources=sources,
                                    score=varia,
                                    rows=rows,
                                    show_table=True,
                                    columns=columns)
        else:

            if selected_action == 'mudaano':
                return render_template('payments_queue.html',
                            acao = selected_action,
                           # rendering
                           page_title=page_title,
                           city_options=city_options,
                           year_options=year_options,
                           days_of_tolerance=days_of_tolerance,
                           user_request=user_request,
                            payment_types=payment_types,


                           selected_city=selected_city,
                                        selected_year=selected_year,
                                        selected_day=int(selected_day),
                                        selected_source=selected_source,
                                        selected_payment=selected_payment)
            
            else:
                selected_day = request.form.get('day', days_of_tolerance[0])

                return render_template('payments_queue.html',
                                        acao = selected_action,
                                        # rendering
                                        page_title=page_title,
                                        city_options=city_options,
                                        year_options=year_options,
                                        days_of_tolerance=days_of_tolerance,
                                        user_request=user_request,
                                        payment_types=payment_types,
                                        
                                        # input
                                        selected_city=selected_city,
                                        selected_year=selected_year,
                                        selected_day=int(selected_day),
                                        selected_source=selected_source,
                                        selected_payment=selected_payment,
                                        

                                        # output
                                        sources=sources)

        

    return render_template('payments_queue.html',
                            acao = selected_action,
                           # rendering
                           page_title=page_title,
                           city_options=city_options,
                           year_options=year_options,
                           days_of_tolerance=days_of_tolerance,
                           user_request=user_request,
                            payment_types=payment_types
                           )


@app.route('/payment_queues_map')
def payment_queues_map():
    queues_map()
    return render_template('payment_queues_map.html')

@app.route('/payment_queues_map2')
def payment_queues_map2():
    queues_map()
    return render_template('payment_queues_map2.html')

if __name__ == '__main__':

    app.run(debug=True)
