from flask import Flask, render_template, request
import pandas as pd
import locale
from static.scripts.Getters import *
from static.scripts.AnaliseScoreUJS import *
from static.scripts.UtilsUJsProcessadas import *
from static.scripts.MontaSagresSimba import *
from static.scripts.utils import *
from static.scripts.FilaP import *
from static.scripts.Plots import *
from static.scripts.Maps import *


locale.getlocale()
('pt_BR', 'UTF-8')

app = Flask(__name__)

df_cities = pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';')

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)


@app.route('/')
def home():
    return render_template('home.html', title='Home')


def output_regular_payments(loan_selected):
    y = loan_selected.listValoresPagamentos
    x = loan_selected.datasPagamentosDateTime
    regular_payments_plot(x, y)

    supplier_id = '{} - ({})'.format(format_cnpj_cpf(loan_selected.cnpj), loan_selected.nmFornecedor)
    
    dates = ' -> '.join([date_to_string(date) for date in loan_selected.datasPagamentosDateTime])
    values = ' -> '.join(map(str, loan_selected.listValoresPagamentos))
    description = loan_selected.descricao

    loan_info = {
        'CPF/CNPJ': supplier_id,
        'Datas': dates,
        'Valores': values,
        'Descrição': description,
    }

    return loan_info


@app.route('/analysis/regular_payments', methods=['GET', 'POST'])
def regular_payments():
    page_title = 'Análise de Pagamentos Regulares'
    options_city = df_cities.Municipio.tolist()
    options_year = [2019, 2020]
    user_request = request.method
    is_post_request = user_request == 'POST'

    if is_post_request:
        selected_city = request.form.get('city')
        selected_year = request.form.get('year')
        selected_supplier = request.form.get('supplier', 0)
        selected_action = request.form.get('action')

        selected_city_id = int(df_cities[df_cities['Municipio'] == selected_city].numUJ)
        loans = get_sorted_loans(selected_city_id, selected_year)
        options_supplier = [str(empenho.nmFornecedor) for empenho in loans]
    
        if selected_action == 'apply':
            supplier_idx = 0
        else:
            supplier_idx = int(selected_supplier)

        loan_selected = loans[supplier_idx]
        loan_info = output_regular_payments(loan_selected)

        return render_template(
            'payments_regular.html',
            page_title=page_title,
            options_city=options_city,
            options_year=options_year,
            user_request=user_request,

            options_supplier=options_supplier,
            loan_info=loan_info,
            selected_city=selected_city,
            selected_year=int(selected_year),
            selected_supplier=int(selected_supplier)
        )

    return render_template(
        'payments_regular.html',
        page_title=page_title,
        options_city=options_city,
        options_year=options_year,
        user_request=user_request
    )


# @app.route('/analysis/service_before_payment', methods=['GET', 'POST'])
# def service_before_payment():
#     page_title = 'Análise de Serviços Antes de Empenho'
#     city_options = list(
#         pd.read_csv('./static/datasets/ListaMunicipios.csv', sep=';').Municipio
#     )
#     year_options = [2019, 2020]
#     user_request = request.method

#     if user_request == 'POST':
#         selected_city = request.form.get('city')
#         selected_year = request.form.get('year')
#         selected_supplier = request.form.get('supplier', 0)
#         selected_action = request.form.get('action')

#         loans = get_servico_emp(selected_city, selected_year)
#         supplier_options = []
#         for idx, loan in enumerate(loans):
#             supplier_options.append(str(idx) + ' - ' + str(loan.nmFornecedor))

#         if selected_action == 'apply':
#             loan_idx = 0
#         elif selected_action == 'update':
#             loan_idx = int(selected_supplier)

#         loan_selected = loans[loan_idx]
#         y = loan_selected.listValoresPagamentos
#         x = loan_selected.datasPagamentosDateTime
#         service_before_payment_plot(x, y)

#         supplier_id = '{} ({})'.format(
#             loan_selected.cnpj, loan_selected.nmFornecedor)
#         dates = '; '.join(
#             map(date_to_string, loan_selected.datasPagamentosDateTime))
#         values = '; '.join(map(str, loan_selected.listValoresPagamentos))
#         description = loan_selected.descricao
#         first_month = str(round(loan_selected.vlMes1, 2))
#         monthly_average = str(round(loan_selected.vlMedioMensal, 2))

#         loan_info = {
#             'CPF/CNPJ': supplier_id,
#             'Datas': dates,
#             'Valores': values,
#             'Descrição': description,
#             'Primeiro Mês': first_month,
#             'Média Mensal': monthly_average
#         }

#         return render_template(
#             'service_before_payment.html',
#             page_title=page_title,
#             city_options=city_options,
#             year_options=year_options,
#             user_request=user_request,

#             supplier_options=supplier_options,
#             loan_info=loan_info,
#             selected_city=selected_city,
#             selected_year=int(selected_year),
#             year=int(selected_year),
#             selected_supplier=int(selected_supplier),
#         )

#     return render_template(
#         'service_before_payment.html',
#         page_title=page_title,
#         city_options=city_options,
#         year_options=year_options,
#         user_request=user_request,
#     )


@app.route('/analysis/simba', methods=['GET', 'POST'])
def simba():
    page_title = 'SIMBA'
    simba_sagres_objects = get_sagres_simba_objects()
    options_entity = ['{} - ({}) - {}'.format(obj.nmFornecedor, format_cnpj_cpf(obj.cpf_cnpj), round(obj.somaSimba - obj.somaSagres, 2)) for obj in simba_sagres_objects]

    selected_entity = int(request.form.get('entity', 0))
    entity = simba_sagres_objects[selected_entity]
    simba_plot(entity)

    sagres_payments = entity.dictPagsMensaisSagres
    simba_payments = entity.dictPagsMensaisSimba
    sagres_rows = []
    simba_rows = []
    for idx in range(1, 13):
        sagres_rows.append(round(sagres_payments[idx], 2))
        simba_rows.append(round(simba_payments[idx], 2))

    entity_info = {'months': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], 'sagres': sagres_rows, 'simba': simba_rows}

    return render_template(
        'simba.html',
        page_title=page_title,

        selected_entity=selected_entity,
        entity_info=entity_info,
        options_entity=options_entity,
    )


@app.route('/analysis/payments_delay', methods=['GET', 'POST'])
def payments_delay():
    page_title = 'Análise de Atraso de Pagamentos'
    options_city = df_cities.Municipio.tolist()
    options_entity_types = {
        'Pessoa Física': 'cpf',
        'Pessoa Jurídica': 'cnpj',
        'Ambos': 'ambos'
    }
    options_entity = list(options_entity_types.keys())
    options_year = [2019, 2020]
    options_limit = [7, 30, 60]
    options_loan_types = {
        'Licitação': 'lic',
        'Dispensado': 'disp',
        'Ambos': 'ambos'
    }
    user_request = request.method
    is_post_request = user_request == 'POST'

    if is_post_request:
        selected_entity = request.form.get('entity')
        selected_year = request.form.get('year')
        selected_limit = request.form.get('limit')
        selected_loan_type = request.form.get('loan_type')
        selected_action = request.form.get('action')
        is_apply_selected = selected_action == 'apply'

        selected_map = generate_delay_map(selected_year, options_loan_types[selected_loan_type], options_entity_types[selected_entity], selected_limit)

        if is_apply_selected:
            selected_city = options_city[0]
        else:
            selected_city = request.form.get('city')
        
        selected_city_num = int(df_cities[df_cities['Municipio'] == selected_city].numUJ)
        options_source = get_delay_sources(selected_year, selected_city_num)

        if is_apply_selected:
            selected_uo_source = options_source[0]
        else:
            selected_uo_source = request.form.get('source')

        selected_uo, selected_source, _ = selected_uo_source.split(' + ')
        df = UJsProcessadas.get_pagamentos_atrasados(
            selected_year,
            options_loan_types[selected_loan_type],
            options_entity_types[selected_entity],
            float(selected_limit),
            selected_city_num,
            selected_uo, selected_source
        )

        plot_data = payments_delay_scatter_plot(df)

        return render_template(
            'payments_delay.html',
            page_title=page_title,
            options_city=options_city,
            options_entity=options_entity,
            options_year=options_year,
            options_limit=options_limit,
            options_loan_types=options_loan_types,
            user_request=user_request,

            options_source=options_source,
            plot_data=plot_data,
            selected_action=selected_action,
            selected_entity=selected_entity,
            selected_city=selected_city,
            selected_year=int(selected_year),
            selected_limit=int(selected_limit),
            selected_uo_source=selected_uo_source,
            selected_loan_type=selected_loan_type,
            selected_map=selected_map
        )

    return render_template(
        'payments_delay.html',
        page_title=page_title,
        options_city=options_city,
        options_entity=options_entity,
        options_year=options_year,
        options_limit=options_limit,
        options_loan_types=options_loan_types,
        user_request=user_request
    )


@app.route('/analysis/nonconformity', methods=['GET', 'POST'])
def nonconformity():
    page_title = 'Análise de Pagamentos Inconformes'
    options_year = [2019, 2020]
    user_request = request.method
    is_post_request = user_request == 'POST'

    if is_post_request:
        selected_year = request.form.get('year')

        rows, cols, links = get_non_conformities(selected_year)
        return render_template(
            'nonconformity.html',
            page_title=page_title,
            options_year=options_year,
            user_request=user_request,

            selected_year=int(selected_year),
            cols=cols,
            rows=rows,
            links=links
        )

    return render_template(
        'nonconformity.html',
        page_title=page_title,
        options_year=options_year,
        user_request=user_request
    )


@app.route('/analysis/matching_sources', methods=['GET', 'POST'])
def matching_sources():
    page_title = 'Correspondência Entre Fontes de Dados'
    options_city = ['Cabo de Santo Agostinho']
    user_request = request.method
    is_post_request = user_request == 'POST'

    if is_post_request:
        selected_city = request.form.get('city')

        cols, rows, cols_general_description, rows_general_description, modals = get_dados_correspondencia(selected_city)

        return render_template(
            'matching_sources.html',
            page_title=page_title,
            options_city=options_city,
            user_request=user_request,

            selected_city=selected_city,
            cols=cols,
            rows=rows,
            rows_general_description=rows_general_description,
            cols_general_description=cols_general_description,
            modals=json.dumps(modals)
        )

    return render_template(
        'matching_sources.html',
        page_title=page_title,
        options_city=options_city,
        user_request=user_request
    )


@app.route('/analysis/payments_queue', methods=['GET', 'POST'])
def payments_queue():
    page_title = 'Filas de Pagamentos'
    city_options = df_cities['Municipio'].tolist()

    year_options = ['2019','2020']
    payment_types = ['Geral','Dispensa','Licitação']

    days_of_tolerance = [7, 30, 60]
    columns = ['Nº Empenho', 'Fornecedor', 'Valor Emp',
               'Valor', 'Data Pag', 'Atraso', 'Qtd ultrapassaram']          
    user_request = request.method
    selected_action = request.form.get('action')
    selected_year = request.form.get('year', year_options[0])
    selected_payment = 'Geral'
    selected_day = days_of_tolerance[0]
    sources = get_lista_UOFR(city_options[0], '2019')

    map = generate_queue_map(selected_year, 'Ge', selected_day)
    is_post_request = user_request == 'POST'

    if is_post_request:
        selected_city = request.form.get('city', city_options[0])
        selected_year = request.form.get('year', year_options[0])
        selected_day = request.form.get('day', int(7))

        selected_action = request.form.get('action')
        
        if (selected_action == 'update2' or selected_action != 'apply') or selected_action != 'update':
            sources = get_lista_UOFR(selected_city, selected_year)
        
        selected_source = request.form.get('source', sources[0])
        formatted_source = ''.join(selected_source.split(' + '))

        selected_payment = request.form.get('payment', payment_types[0])
        cities_num = int(df_cities[df_cities['Municipio'] == selected_city].numUJ)

        map = generate_queue_map( selected_year, selected_payment[0:2], selected_day)

        if selected_action == 'apply' or selected_action == 'update':

            selected_payment_type = request.form.get('payment', payment_types[0])
            rows, varia = MudaMunicio(cities_num, formatted_source, int(selected_day), selected_year, selected_payment_type)

            return render_template(
                'payments_queue.html',
                page_title=page_title,
                city_options=city_options,
                year_options=year_options,
                days_of_tolerance=days_of_tolerance,
                user_request=user_request,
                payment_types=payment_types,
                
                map = map,
                acao = selected_action,
                selected_city=selected_city,
                selected_year=selected_year,
                selected_day=int(selected_day),
                selected_source=selected_source,
                selected_payment=selected_payment,
                
                sources=sources,
                score=varia,
                rows=rows,
                show_table=True,
                columns=columns
            )
        else:

            if selected_action == 'mudaano':
                return render_template(
                    'payments_queue.html',
                    page_title=page_title,
                    city_options=city_options,
                    year_options=year_options,
                    days_of_tolerance=days_of_tolerance,
                    user_request=user_request,
                    payment_types=payment_types,

                    map = map,
                    acao = selected_action,
                    selected_city=selected_city,
                    selected_year=selected_year,
                    selected_day=int(selected_day),
                    selected_source=selected_source,
                    selected_payment=selected_payment
                )
            
            else:
                return render_template(
                    'payments_queue.html',
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
                    selected_payment=selected_payment,
                    sources=sources,
                    map = map,
                    acao = selected_action,
                )

    return render_template(
        'payments_queue.html',
        page_title=page_title,
        city_options=city_options,
        year_options=year_options,
        days_of_tolerance=days_of_tolerance,
        user_request=user_request,
        payment_types=payment_types,

        map = map,
        acao = selected_action
    )


if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)
